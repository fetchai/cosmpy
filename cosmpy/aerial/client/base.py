# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Functionality shared between the sync and async ledger clients.

Everything in this module is I/O free: configuration handling, request/response
translation and fee arithmetic. The network calls themselves live in the
concrete clients (``LedgerClient`` and ``AsyncLedgerClient``), which both
operate on the same generated protobuf stubs.
"""

import math
from datetime import timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union

import certifi
import grpc
from dateutil.parser import isoparse
from packaging.version import Version

from cosmpy.aerial import cast_to_int
from cosmpy.aerial.client.staking import (
    StakingPosition,
    UnbondingPositions,
    Validator,
    ValidatorStatus,
)
from cosmpy.aerial.client.utils import ensure_timedelta
from cosmpy.aerial.coins import Coin
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx import Transaction, TxState
from cosmpy.aerial.tx_helpers import MessageLog, TxResponse, safe_decode
from cosmpy.aerial.types import Account, NodeInfo
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthGrpcClient
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankGrpcClient
from cosmpy.protos.cosmos.base.tendermint.v1beta1.query_pb2_grpc import (
    ServiceStub as TendermintQueryGrpcClient,
)
from cosmpy.protos.cosmos.consensus.v1.query_pb2_grpc import (
    QueryStub as QueryConsensusGrpcClient,
)
from cosmpy.protos.cosmos.crypto.ed25519.keys_pb2 import (  # noqa # pylint: disable=unused-import
    PubKey,
)
from cosmpy.protos.cosmos.distribution.v1beta1.query_pb2_grpc import (
    QueryStub as DistributionGrpcClient,
)
from cosmpy.protos.cosmos.params.v1beta1.query_pb2_grpc import (
    QueryStub as QueryParamsGrpcClient,
)
from cosmpy.protos.cosmos.staking.v1beta1.query_pb2_grpc import (
    QueryStub as StakingGrpcClient,
)
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2_grpc import (
    QueryStub as CosmWasmGrpcClient,
)


DEFAULT_QUERY_TIMEOUT_SECS = 15
DEFAULT_QUERY_INTERVAL_SECS = 2
COSMOS_SDK_DEC_COIN_PRECISION = 10**18


class LedgerClientBase:
    """Ledger client base with the functionality shared by the sync and async clients."""

    # query stubs, wired to gRPC or REST backends by the concrete clients
    wasm: Any
    auth: Any
    txs: Any
    bank: Any
    staking: Any
    distribution: Any
    params: Any
    consensus: Any
    tendermint: Any

    def __init__(
        self,
        cfg: NetworkConfig,
        query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
        query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS,
    ):
        """Init ledger client base.

        :param cfg: Network configurations
        :param query_interval_secs: int. optional interval int seconds
        :param query_timeout_secs: int. optional interval int seconds
        """
        self._query_interval_secs = query_interval_secs
        self._query_timeout_secs = query_timeout_secs
        cfg.validate()
        self._network_config = cfg

    @property
    def network_config(self) -> NetworkConfig:
        """Get the network config.

        :return: network config
        """
        return self._network_config

    def _init_grpc_stubs(self, grpc_client):
        """Create the generated protobuf stubs on the given channel.

        The generated stub classes work with both a synchronous ``grpc.Channel``
        and an asynchronous ``grpc.aio.Channel``: with the latter, the stub
        methods return awaitables.

        :param grpc_client: gRPC channel (sync or aio)
        """
        self.wasm = CosmWasmGrpcClient(grpc_client)
        self.auth = AuthGrpcClient(grpc_client)
        self.txs = TxGrpcClient(grpc_client)
        self.bank = BankGrpcClient(grpc_client)
        self.staking = StakingGrpcClient(grpc_client)
        self.distribution = DistributionGrpcClient(grpc_client)
        self.params = QueryParamsGrpcClient(grpc_client)
        self.consensus = QueryConsensusGrpcClient(grpc_client)
        self.tendermint = TendermintQueryGrpcClient(grpc_client)

    @staticmethod
    def _create_ssl_credentials() -> grpc.ChannelCredentials:
        """Create SSL channel credentials using the certifi CA bundle.

        :return: gRPC channel credentials
        """
        with open(certifi.where(), "rb") as f:
            trusted_certs = f.read()
        return grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    # NOTE(pb): We should come up with a mechanism how this method (or a new one) can return also `Coin`, resp. `Coins`.
    def estimate_fee_from_gas(self, gas_limit: int) -> str:
        """Estimate fee from gas.

        :param gas_limit: gas limit
        :return: Estimated fee for transaction
        """
        fee = math.ceil(gas_limit * self.network_config.fee_minimum_gas_price)
        return f"{fee}{self.network_config.fee_denomination}"

    def _resolve_tx_poll_timings(
        self,
        timeout: Optional[Union[int, float, timedelta]],
        poll_period: Optional[Union[int, float, timedelta]],
    ) -> Tuple[timedelta, timedelta]:
        """Resolve tx polling timeout and poll period, falling back to client defaults.

        :param timeout: optional timeout
        :param poll_period: optional poll period
        :return: timeout and poll period timedeltas
        """
        resolved_timeout = (
            ensure_timedelta(timeout)
            if timeout
            else timedelta(seconds=self._query_timeout_secs)
        )
        resolved_poll_period = (
            ensure_timedelta(poll_period)
            if poll_period
            else timedelta(seconds=self._query_interval_secs)
        )
        return resolved_timeout, resolved_poll_period

    @staticmethod
    def _parse_account(response: Any, address: Address) -> Account:
        """Parse a QueryAccountResponse into an Account.

        :param response: query account response
        :param address: queried address
        :raises RuntimeError: Unexpected account type returned from query
        :return: account details
        """
        account = BaseAccount()
        if not response.account.Is(BaseAccount.DESCRIPTOR):
            raise RuntimeError("Unexpected account type returned from query")
        response.account.Unpack(account)

        return Account(
            address=address,
            number=account.account_number,
            sequence=account.sequence,
        )

    @staticmethod
    def _parse_node_info(response: Any) -> NodeInfo:
        """Parse a GetNodeInfoResponse into a NodeInfo.

        :param response: get node info response
        :return: NodeInfo
        """
        cosmos_sdk_version = Version(
            response.application_version.cosmos_sdk_version.lstrip("v")
        )
        app_name = response.application_version.name
        app_version = Version(response.application_version.version.lstrip("v"))

        return NodeInfo(
            cosmos_sdk_version=cosmos_sdk_version,
            app_name=app_name,
            app_version=app_version,
        )

    @staticmethod
    def _parse_bank_balance(resp: Any, denom: str) -> int:
        """Parse a QueryBalanceResponse into an amount.

        :param resp: query balance response
        :param denom: queried denomination
        :return: balance amount
        """
        assert resp.balance.denom == denom  # sanity check
        return int(resp.balance.amount)

    @staticmethod
    def _parse_bank_all_balances(resp: Any) -> List[Coin]:
        """Parse a QueryAllBalancesResponse into a list of coins.

        :param resp: query all balances response
        :return: list of coins
        """
        return [Coin(amount=coin.amount, denom=coin.denom) for coin in resp.balances]

    @staticmethod
    def _parse_validators(resp: Any) -> List[Validator]:
        """Parse a QueryValidatorsResponse into a list of validators.

        :param resp: query validators response
        :return: list of validators
        """
        validators: List[Validator] = []
        for validator in resp.validators:
            validators.append(
                Validator(
                    address=Address(validator.operator_address),
                    tokens=cast_to_int(validator.tokens, False),
                    moniker=str(validator.description.moniker),
                    status=ValidatorStatus.from_proto(validator.status),
                )
            )
        return validators

    def _parse_staking_position(self, item: Any, rewards_resp: Any) -> StakingPosition:
        """Build a StakingPosition from a delegation item and its rewards response.

        :param item: delegation response item
        :param rewards_resp: delegation rewards response
        :return: staking position
        """
        stake_reward_dec = Decimal(0)
        stake_reward = 0
        for reward in rewards_resp.rewards:
            if reward.denom == self.network_config.staking_denomination:
                stake_reward_dec = Decimal(reward.amount)
                stake_reward = cast_to_int(reward.amount, False)
                break

        return StakingPosition(
            validator=Address(item.delegation.validator_address),
            amount=cast_to_int(item.balance.amount, False),
            reward=stake_reward,
            reward_dec=stake_reward_dec,
        )

    @staticmethod
    def _build_unbonding_positions(
        unbonding_pages: List[Any],
    ) -> List[UnbondingPositions]:
        """Build the list of unbonding positions from paginated unbonding responses.

        :param unbonding_pages: pages of DelegatorUnbondingDelegations responses
        :return: list of unbonding positions
        """
        unbonding_summary: Dict[str, int] = {}
        for resp in unbonding_pages:
            for item in resp.unbonding_responses:
                validator = str(item.validator_address)
                total_unbonding = unbonding_summary.get(validator, 0)

                for entry in item.entries:
                    total_unbonding += cast_to_int(entry.balance, False)

                unbonding_summary[validator] = total_unbonding

        # build the final list of unbonding positions
        unbonding_positions: List[UnbondingPositions] = []
        for validator, total_unbonding in unbonding_summary.items():
            unbonding_positions.append(
                UnbondingPositions(
                    validator=Address(validator),
                    amount=total_unbonding,
                )
            )
        return unbonding_positions

    @staticmethod
    def _is_tx_not_found_error(error: Exception) -> bool:
        """Check whether a failed GetTx call indicates a missing transaction.

        :param error: exception raised by the GetTx call
        :return: True if the error indicates the tx is not (yet) found
        """
        if isinstance(error, grpc.RpcError):
            return "not found" in error.details()
        details = str(error)
        return "tx" in details and "not found" in details

    @staticmethod
    def _check_tx_final_for_simulation(tx: Transaction):
        """Ensure the transaction can be simulated.

        :param tx: transaction
        :raises RuntimeError: Unable to simulate non final transaction
        """
        if tx.state != TxState.Final:
            raise RuntimeError("Unable to simulate non final transaction")

    @staticmethod
    def _parse_tx_response(tx_response: Any) -> TxResponse:
        # parse the transaction logs
        logs = []
        for log_data in tx_response.logs:
            events = {}
            for event in log_data.events:
                events[event.type] = {a.key: a.value for a in event.attributes}
            logs.append(
                MessageLog(
                    index=int(log_data.msg_index), log=log_data.msg_index, events=events
                )
            )

        # parse the transaction events
        events = {}
        for event in tx_response.events:
            event_data = events.get(event.type, {})
            for attribute in event.attributes:
                event_data[safe_decode(attribute.key)] = safe_decode(attribute.value)
            events[event.type] = event_data

        timestamp = None
        if tx_response.timestamp:
            timestamp = isoparse(tx_response.timestamp)

        return TxResponse(
            hash=str(tx_response.txhash),
            height=int(tx_response.height),
            code=int(tx_response.code),
            gas_wanted=int(tx_response.gas_wanted),
            gas_used=int(tx_response.gas_used),
            raw_log=str(tx_response.raw_log),
            logs=logs,
            events=events,
            timestamp=timestamp,
        )

    @classmethod
    def _check_broadcast_response(cls, resp: Any) -> str:
        """Check a BroadcastTxResponse and return the tx digest.

        :param resp: broadcast tx response
        :return: transaction digest
        """
        tx_digest = resp.tx_response.txhash

        # check that the response is successful
        initial_tx_response = cls._parse_tx_response(resp.tx_response)
        initial_tx_response.ensure_successful()

        return tx_digest
