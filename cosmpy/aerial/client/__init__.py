# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
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

"""Client functionality."""
import json
import time
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

import grpc

from cosmpy.aerial.client.bank import create_bank_send_msg
from cosmpy.aerial.client.base import (  # noqa: F401 # pylint: disable=unused-import
    COSMOS_SDK_DEC_COIN_PRECISION,
    DEFAULT_QUERY_INTERVAL_SECS,
    DEFAULT_QUERY_TIMEOUT_SECS,
    LedgerClientBase,
)
from cosmpy.aerial.client.distribution import create_withdraw_delegator_reward
from cosmpy.aerial.client.staking import (
    StakingSummary,
    Validator,
    ValidatorStatus,
    create_delegate_msg,
    create_redelegate_msg,
    create_undelegate_msg,
)
from cosmpy.aerial.client.utils import (
    TxFee,
    get_paginated,
    prepare_and_broadcast_basic_transaction,
)
from cosmpy.aerial.coins import Coin
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.exceptions import NotFoundError, QueryTimeoutError
from cosmpy.aerial.gas import GasStrategy, SimulationGasStrategy
from cosmpy.aerial.query_client import wrap_query_client
from cosmpy.aerial.query_context import ResponseQueryContext
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.tx_helpers import SubmittedTx, TxResponse
from cosmpy.aerial.types import Account, Block, NodeInfo
from cosmpy.aerial.urls import Protocol, parse_url
from cosmpy.aerial.wallet import Wallet
from cosmpy.auth.rest_client import AuthRestClient
from cosmpy.bank.rest_client import BankRestClient
from cosmpy.common.rest_client import RestClient
from cosmpy.consensus.rest_client import ConsensusRestClient
from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
from cosmpy.crypto.address import Address
from cosmpy.distribution.rest_client import DistributionRestClient
from cosmpy.params.rest_client import ParamsRestClient
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import (
    QueryAllBalancesRequest,
    QueryBalanceRequest,
)
from cosmpy.protos.cosmos.base.tendermint.v1beta1.query_pb2 import (
    GetBlockByHeightRequest,
    GetLatestBlockRequest,
    GetNodeInfoRequest,
)
from cosmpy.protos.cosmos.distribution.v1beta1.query_pb2 import (
    QueryDelegationRewardsRequest,
)
from cosmpy.protos.cosmos.params.v1beta1.query_pb2 import QueryParamsRequest
from cosmpy.protos.cosmos.staking.v1beta1.query_pb2 import (
    QueryDelegatorDelegationsRequest,
    QueryDelegatorUnbondingDelegationsRequest,
    QueryValidatorsRequest,
)
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import (
    BroadcastMode,
    BroadcastTxRequest,
    GetTxRequest,
    SimulateRequest,
)
from cosmpy.staking.rest_client import StakingRestClient
from cosmpy.tendermint.rest_client import (
    CosmosBaseTendermintRestClient as TendermintRestClient,
)
from cosmpy.tx.rest_client import TxRestClient


class LedgerClient(LedgerClientBase):
    """Ledger client."""

    def __init__(
        self,
        cfg: NetworkConfig,
        query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
        query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS,
    ):
        """Init ledger client.

        :param cfg: Network configurations
        :param query_interval_secs: int. optional interval int seconds
        :param query_timeout_secs: int. optional interval int seconds
        """
        super().__init__(cfg, query_interval_secs, query_timeout_secs)
        self._gas_strategy: GasStrategy = SimulationGasStrategy(self)
        self._init_clients()

    def _init_clients(self):
        """Initialize transport-specific module clients."""
        cfg = self.network_config

        parsed_url = parse_url(cfg.url)

        if parsed_url.protocol == Protocol.GRPC:
            if parsed_url.secure:
                credentials = self._create_ssl_credentials()
                grpc_client = grpc.secure_channel(parsed_url.host_and_port, credentials)
            else:
                grpc_client = grpc.insecure_channel(parsed_url.host_and_port)

            self._init_grpc_stubs(grpc_client)
            self._wrap_query_clients()
        else:
            rest_client = RestClient(parsed_url.rest_url)

            self.wasm = wrap_query_client(CosmWasmRestClient(rest_client))  # type: ignore
            self.auth = wrap_query_client(AuthRestClient(rest_client))  # type: ignore
            self.txs = wrap_query_client(TxRestClient(rest_client))  # type: ignore
            self.bank = wrap_query_client(BankRestClient(rest_client))  # type: ignore
            self.staking = wrap_query_client(StakingRestClient(rest_client))  # type: ignore
            self.distribution = wrap_query_client(DistributionRestClient(rest_client))  # type: ignore
            self.params = wrap_query_client(ParamsRestClient(rest_client))  # type: ignore
            self.consensus = wrap_query_client(ConsensusRestClient(rest_client))  # type: ignore
            self.tendermint = wrap_query_client(TendermintRestClient(rest_client))  # type: ignore

    def _wrap_query_clients(self):
        """Wrap module clients so query methods accept request-scoped context."""
        self.wasm = wrap_query_client(self.wasm)
        self.auth = wrap_query_client(self.auth)
        self.txs = wrap_query_client(self.txs)
        self.bank = wrap_query_client(self.bank)
        self.staking = wrap_query_client(self.staking)
        self.distribution = wrap_query_client(self.distribution)
        self.params = wrap_query_client(self.params)
        self.consensus = wrap_query_client(self.consensus)
        self.tendermint = wrap_query_client(self.tendermint)

    @property
    def gas_strategy(self) -> GasStrategy:
        """Get gas strategy.

        :return: gas strategy
        """
        return self._gas_strategy

    @gas_strategy.setter
    def gas_strategy(self, strategy: GasStrategy):
        """Set gas strategy.

        :param strategy: strategy
        :raises RuntimeError: Invalid strategy must implement GasStrategy interface
        """
        if not isinstance(strategy, GasStrategy):
            raise RuntimeError("Invalid strategy must implement GasStrategy interface")
        self._gas_strategy = strategy

    def query_account(
        self, address: Address, ctx: Optional[ResponseQueryContext] = None
    ) -> Account:
        """Query account.

        :param address: address
        :param ctx: Optional QueryContext
        :return: account details
        """
        request = QueryAccountRequest(address=str(address))
        response = self.auth.Account(request, ctx=ctx)
        return self._parse_account(response, address)

    def query_params(
        self,
        subspace: str,
        key: str,
        ctx: Optional[ResponseQueryContext] = None,
    ) -> Any:
        """Query Prams.

        :param subspace: subspace
        :param key: key
        :param ctx: Optional QueryContext
        :return: Query params
        """
        req = QueryParamsRequest(subspace=subspace, key=key)
        resp = self.params.Params(req, ctx=ctx)
        return json.loads(resp.param.value)

    def query_node_info(self, ctx: Optional[ResponseQueryContext] = None) -> NodeInfo:
        """
        Query basic Tendermint / node information (moniker, chain-id, version, etc.).

        :param ctx: Optional QueryContext

        :return: NodeInfo.
        """
        request = GetNodeInfoRequest()
        response = self.tendermint.GetNodeInfo(request, ctx=ctx)
        return self._parse_node_info(response)

    def query_consensus_params(self, ctx: Optional[ResponseQueryContext] = None) -> Any:
        """Query consensus params.

        :param ctx: Optional QueryContext
        :return: Query consensus params
        """
        req = QueryParamsRequest()
        resp = self.consensus.Params(req, ctx=ctx)
        return resp

    def query_bank_balance(
        self,
        address: Address,
        denom: Optional[str] = None,
        ctx: Optional[ResponseQueryContext] = None,
    ) -> int:
        """Query bank balance.

        :param ctx: Optional QueryContext
        :param address: address
        :param denom: denom, defaults to None
        :return: bank balance
        """
        denom = denom or self.network_config.fee_denomination

        req = QueryBalanceRequest(
            address=str(address),
            denom=denom,
        )

        resp = self.bank.Balance(req, ctx=ctx)
        return self._parse_bank_balance(resp, denom)

    def query_bank_all_balances(
        self, address: Address, ctx: Optional[ResponseQueryContext] = None
    ) -> List[Coin]:
        """Query bank all balances.

        :param ctx: Optional QueryContext
        :param address: address
        :return: bank all balances
        """
        req = QueryAllBalancesRequest(address=str(address))
        resp = self.bank.AllBalances(req, ctx=ctx)
        return self._parse_bank_all_balances(resp)

    def send_tokens(
        self,
        destination: Address,
        amount: int,
        denom: str,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Send tokens.

        :param destination: destination address
        :param amount: amount
        :param denom: denom
        :param sender: sender
        :param memo: memo, defaults to None
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        # build up the store transaction
        tx = Transaction()
        tx.add_message(
            create_bank_send_msg(sender.address(), destination, amount, denom)
        )

        return prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    def query_validators(
        self,
        status: Optional[ValidatorStatus] = None,
        ctx: Optional[ResponseQueryContext] = None,
    ) -> List[Validator]:
        """Query validators.

        :param status: validator status, defaults to None
        :param ctx: Optional QueryContext
        :return: List of validators
        """
        filtered_status = status or ValidatorStatus.BONDED

        req = QueryValidatorsRequest()
        if filtered_status != ValidatorStatus.UNSPECIFIED:
            req.status = filtered_status.value

        resp = self.staking.Validators(req, ctx=ctx)
        return self._parse_validators(resp)

    def query_staking_summary(
        self, address: Address, ctx: Optional[ResponseQueryContext] = None
    ) -> StakingSummary:
        """Query staking summary.

        :param address: address
        :param ctx: Optional QueryContext
        :return: staking summary
        """
        current_positions = []

        req = QueryDelegatorDelegationsRequest(delegator_addr=str(address))

        for resp in get_paginated(
            req, self.staking.DelegatorDelegations, per_page_limit=1, ctx=ctx
        ):
            for item in resp.delegation_responses:
                req = QueryDelegationRewardsRequest(
                    delegator_address=str(address),
                    validator_address=str(item.delegation.validator_address),
                )
                rewards_resp = self.distribution.DelegationRewards(req, ctx=ctx)

                current_positions.append(
                    self._parse_staking_position(item, rewards_resp)
                )

        req = QueryDelegatorUnbondingDelegationsRequest(delegator_addr=str(address))
        unbonding_pages = get_paginated(
            req, self.staking.DelegatorUnbondingDelegations, ctx=ctx
        )

        return StakingSummary(
            current_positions=current_positions,
            unbonding_positions=self._build_unbonding_positions(unbonding_pages),
        )

    def delegate_tokens(
        self,
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Delegate tokens.

        :param validator: validator address
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_delegate_msg(
                sender.address(),
                validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    def redelegate_tokens(
        self,
        current_validator: Address,
        next_validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Redelegate tokens.

        :param current_validator: current validator address
        :param next_validator: next validator address
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_redelegate_msg(
                sender.address(),
                current_validator,
                next_validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    def undelegate_tokens(
        self,
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Undelegate tokens.

        :param validator: validator
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_undelegate_msg(
                sender.address(),
                validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    def claim_rewards(
        self,
        validator: Address,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """claim rewards.

        :param validator: validator
        :param sender: sender
        :param memo: memo, defaults to None
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(create_withdraw_delegator_reward(sender.address(), validator))

        return prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    def estimate_gas_for_tx(self, tx: Transaction) -> int:
        """Estimate gas for transaction.

        :param tx: transaction
        :return: Estimated gas for transaction
        """
        return self._gas_strategy.estimate_gas(tx)

    # NOTE(pb): We should come up with a mechanism how this method (or a new one) can return also `Coin`, resp. `Coins`.
    def estimate_gas_and_fee_for_tx(self, tx: Transaction) -> Tuple[int, str]:
        """Estimate gas and fee for transaction.

        :param tx: transaction
        :return: estimate gas, fee for transaction
        """
        gas_estimate = self.estimate_gas_for_tx(tx)
        fee = self.estimate_fee_from_gas(gas_estimate)
        return gas_estimate, fee

    def wait_for_query_tx(
        self,
        tx_hash: str,
        timeout: Optional[timedelta] = None,
        poll_period: Optional[timedelta] = None,
        ctx: Optional[ResponseQueryContext] = None,
    ) -> TxResponse:
        """Wait for query transaction.

        :param tx_hash: transaction hash
        :param timeout: timeout, defaults to None
        :param poll_period: poll_period, defaults to None
        :param ctx: Optional QueryContext

        :raises QueryTimeoutError: timeout

        :return: transaction response
        """
        timeout, poll_period = self._resolve_tx_poll_timings(timeout, poll_period)

        start = datetime.now()
        while True:
            try:
                return self.query_tx(tx_hash, ctx=ctx)
            except NotFoundError:
                pass

            delta = datetime.now() - start
            if delta >= timeout:
                raise QueryTimeoutError()

            time.sleep(poll_period.total_seconds())

    def query_tx(
        self, tx_hash: str, ctx: Optional[ResponseQueryContext] = None
    ) -> TxResponse:
        """query transaction.

        :param tx_hash: transaction hash
        :param ctx: Optional QueryContext
        :raises NotFoundError: Tx details not found
        :raises grpc.RpcError: RPC connection issue
        :return: query response
        """
        req = GetTxRequest(hash=tx_hash)
        try:
            resp = self.txs.GetTx(req, ctx=ctx)
        except grpc.RpcError as e:
            if self._is_tx_not_found_error(e):
                raise NotFoundError() from e
            raise
        except RuntimeError as e:
            if self._is_tx_not_found_error(e):
                raise NotFoundError() from e
            raise

        return self._parse_tx_response(resp.tx_response)

    def simulate_tx(self, tx: Transaction) -> int:
        """simulate transaction.

        :param tx: transaction
        :return: gas used in transaction
        """
        self._check_tx_final_for_simulation(tx)

        req = SimulateRequest(tx=tx.tx)
        resp = self.txs.Simulate(req)

        return int(resp.gas_info.gas_used)

    def broadcast_tx(self, tx: Transaction) -> SubmittedTx:
        """Broadcast transaction.

        :param tx: transaction
        :return: Submitted transaction
        """
        # create the broadcast request
        broadcast_req = BroadcastTxRequest(
            tx_bytes=tx.tx.SerializeToString(), mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        # broadcast the transaction
        resp = self.txs.BroadcastTx(broadcast_req)
        tx_digest = self._check_broadcast_response(resp)

        return SubmittedTx(self, tx_digest)

    def query_latest_block(self, ctx: Optional[ResponseQueryContext] = None) -> Block:
        """Query the latest block.

        :param ctx: Optional QueryContext
        :return: latest block
        """
        req = GetLatestBlockRequest()
        resp = self.tendermint.GetLatestBlock(req, ctx=ctx)
        return Block.from_proto(resp.block)

    def query_block(
        self, height: int, ctx: Optional[ResponseQueryContext] = None
    ) -> Block:
        """Query the block.

        :param height: block height
        :param ctx: Optional QueryContext
        :return: block
        """
        req = GetBlockByHeightRequest(height=height)
        resp = self.tendermint.GetBlockByHeight(req, ctx=ctx)
        return Block.from_proto(resp.block)

    def query_height(self, ctx: Optional[ResponseQueryContext] = None) -> int:
        """Query the latest block height.

        :return: latest block height
        """
        return self.query_latest_block(ctx=ctx).height

    def query_chain_id(self, ctx: Optional[ResponseQueryContext] = None) -> str:
        """Query the chain id.

        :param ctx: Optional QueryContext
        :return: chain id
        """
        return self.query_latest_block(ctx=ctx).chain_id
