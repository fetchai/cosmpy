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

"""Asyncio-native client functionality (gRPC endpoints only).

``AsyncLedgerClient`` mirrors ``LedgerClient`` method for method, but performs
all network I/O on grpc's native asyncio channel (``grpc.aio``) — no worker
threads involved. It reuses the same generated protobuf stubs as the sync
client; the stubs return awaitables when constructed over an aio channel.

Note: instantiate the client from within a running event loop (i.e. inside the
coroutine passed to ``asyncio.run``) — the underlying grpc.aio channel binds to
the running loop when it is created.

Usage:

.. code-block:: python

    async with AsyncLedgerClient(NetworkConfig.fetchai_mainnet()) as client:
        balance = await client.query_bank_balance(address)
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional, Tuple, Union

import grpc
from grpc import aio

from cosmpy.aerial.client.bank import create_bank_send_msg
from cosmpy.aerial.client.base import (
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
from cosmpy.aerial.client.utils import DEFAULT_PER_PAGE_LIMIT
from cosmpy.aerial.coins import Coin
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.exceptions import NotFoundError, QueryTimeoutError
from cosmpy.aerial.gas import AsyncGasStrategy, AsyncSimulationGasStrategy, GasStrategy
from cosmpy.aerial.tx import SigningCfg, Transaction, TxFee
from cosmpy.aerial.tx_helpers import AsyncSubmittedTx, TxResponse
from cosmpy.aerial.types import Account, Block, NodeInfo
from cosmpy.aerial.urls import Protocol, parse_url
from cosmpy.aerial.wallet import Wallet
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import (
    QueryAllBalancesRequest,
    QueryBalanceRequest,
)
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
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


class AsyncLedgerClient(LedgerClientBase):
    """Asyncio-native ledger client (gRPC endpoints only)."""

    def __init__(
        self,
        cfg: NetworkConfig,
        query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
        query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS,
    ):
        """Init async ledger client.

        :param cfg: Network configurations
        :param query_interval_secs: int. optional interval int seconds
        :param query_timeout_secs: int. optional interval int seconds
        :raises RuntimeError: Network config url is not a gRPC endpoint
        """
        super().__init__(cfg, query_interval_secs, query_timeout_secs)
        self._gas_strategy: Union[
            GasStrategy, AsyncGasStrategy
        ] = AsyncSimulationGasStrategy(self)

        parsed_url = parse_url(cfg.url)

        if parsed_url.protocol != Protocol.GRPC:
            raise RuntimeError(
                "AsyncLedgerClient supports gRPC endpoints only; "
                f"got {cfg.url!r}. Use LedgerClient for REST endpoints."
            )

        if parsed_url.secure:
            credentials = self._create_ssl_credentials()
            self._grpc_channel = aio.secure_channel(
                parsed_url.host_and_port, credentials
            )
        else:
            self._grpc_channel = aio.insecure_channel(parsed_url.host_and_port)

        self._init_grpc_stubs(self._grpc_channel)

    async def close(self):
        """Close the underlying gRPC channel."""
        await self._grpc_channel.close()

    async def __aenter__(self) -> "AsyncLedgerClient":
        """Enter the async context.

        :return: this client
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Exit the async context, closing the gRPC channel.

        :param exc_type: exception type
        :param exc_value: exception value
        :param traceback: exception traceback
        """
        await self.close()

    @property
    def gas_strategy(self) -> Union[GasStrategy, AsyncGasStrategy]:
        """Get gas strategy.

        :return: gas strategy
        """
        return self._gas_strategy

    @gas_strategy.setter
    def gas_strategy(self, strategy: Union[GasStrategy, AsyncGasStrategy]):
        """Set gas strategy.

        :param strategy: strategy
        :raises RuntimeError: Invalid strategy must implement GasStrategy or AsyncGasStrategy interface
        """
        if not isinstance(strategy, (GasStrategy, AsyncGasStrategy)):
            raise RuntimeError(
                "Invalid strategy must implement GasStrategy or AsyncGasStrategy interface"
            )
        self._gas_strategy = strategy

    async def query_account(self, address: Address) -> Account:
        """Query account.

        :param address: address
        :return: account details
        """
        request = QueryAccountRequest(address=str(address))
        response = await self.auth.Account(request)
        return self._parse_account(response, address)

    async def query_params(self, subspace: str, key: str) -> Any:
        """Query Prams.

        :param subspace: subspace
        :param key: key
        :return: Query params
        """
        req = QueryParamsRequest(subspace=subspace, key=key)
        resp = await self.params.Params(req)
        return json.loads(resp.param.value)

    async def query_node_info(self) -> NodeInfo:
        """
        Query basic Tendermint / node information (moniker, chain-id, version, etc.).

        :return: NodeInfo.
        """
        request = GetNodeInfoRequest()
        response = await self.tendermint.GetNodeInfo(request)
        return self._parse_node_info(response)

    async def query_consensus_params(self) -> Any:
        """Query consensus params.

        :return: Query consensus params
        """
        req = QueryParamsRequest()
        resp = await self.consensus.Params(req)
        return resp

    async def query_bank_balance(
        self, address: Address, denom: Optional[str] = None
    ) -> int:
        """Query bank balance.

        :param address: address
        :param denom: denom, defaults to None
        :return: bank balance
        """
        denom = denom or self.network_config.fee_denomination

        req = QueryBalanceRequest(
            address=str(address),
            denom=denom,
        )

        resp = await self.bank.Balance(req)
        return self._parse_bank_balance(resp, denom)

    async def query_bank_all_balances(self, address: Address) -> List[Coin]:
        """Query bank all balances.

        :param address: address
        :return: bank all balances
        """
        req = QueryAllBalancesRequest(address=str(address))
        resp = await self.bank.AllBalances(req)
        return self._parse_bank_all_balances(resp)

    async def send_tokens(
        self,
        destination: Address,
        amount: int,
        denom: str,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
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

        return await prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    async def query_validators(
        self, status: Optional[ValidatorStatus] = None
    ) -> List[Validator]:
        """Query validators.

        :param status: validator status, defaults to None
        :return: List of validators
        """
        filtered_status = status or ValidatorStatus.BONDED

        req = QueryValidatorsRequest()
        if filtered_status != ValidatorStatus.UNSPECIFIED:
            req.status = filtered_status.value

        resp = await self.staking.Validators(req)
        return self._parse_validators(resp)

    async def query_staking_summary(self, address: Address) -> StakingSummary:
        """Query staking summary.

        :param address: address
        :return: staking summary
        """
        current_positions = []

        req = QueryDelegatorDelegationsRequest(delegator_addr=str(address))

        for resp in await get_paginated(
            req, self.staking.DelegatorDelegations, per_page_limit=1
        ):
            for item in resp.delegation_responses:
                req = QueryDelegationRewardsRequest(
                    delegator_address=str(address),
                    validator_address=str(item.delegation.validator_address),
                )
                rewards_resp = await self.distribution.DelegationRewards(req)

                current_positions.append(
                    self._parse_staking_position(item, rewards_resp)
                )

        req = QueryDelegatorUnbondingDelegationsRequest(delegator_addr=str(address))
        unbonding_pages = await get_paginated(
            req, self.staking.DelegatorUnbondingDelegations
        )

        return StakingSummary(
            current_positions=current_positions,
            unbonding_positions=self._build_unbonding_positions(unbonding_pages),
        )

    async def delegate_tokens(
        self,
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
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

        return await prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    async def redelegate_tokens(
        self,
        current_validator: Address,
        next_validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
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

        return await prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    async def undelegate_tokens(
        self,
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
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

        return await prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    async def claim_rewards(
        self,
        validator: Address,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
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

        return await prepare_and_broadcast_basic_transaction(
            self,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )

    async def estimate_gas_for_tx(self, tx: Transaction) -> int:
        """Estimate gas for transaction.

        Supports both async and (I/O-free) sync gas strategies.

        :param tx: transaction
        :return: Estimated gas for transaction
        """
        if isinstance(self._gas_strategy, AsyncGasStrategy):
            return await self._gas_strategy.estimate_gas(tx)
        return self._gas_strategy.estimate_gas(tx)

    # NOTE(pb): We should come up with a mechanism how this method (or a new one) can return also `Coin`, resp. `Coins`.
    async def estimate_gas_and_fee_for_tx(self, tx: Transaction) -> Tuple[int, str]:
        """Estimate gas and fee for transaction.

        :param tx: transaction
        :return: estimate gas, fee for transaction
        """
        gas_estimate = await self.estimate_gas_for_tx(tx)
        fee = self.estimate_fee_from_gas(gas_estimate)
        return gas_estimate, fee

    async def wait_for_query_tx(
        self,
        tx_hash: str,
        timeout: Optional[timedelta] = None,
        poll_period: Optional[timedelta] = None,
    ) -> TxResponse:
        """Wait for query transaction.

        :param tx_hash: transaction hash
        :param timeout: timeout, defaults to None
        :param poll_period: poll_period, defaults to None

        :raises QueryTimeoutError: timeout

        :return: transaction response
        """
        timeout, poll_period = self._resolve_tx_poll_timings(timeout, poll_period)

        start = datetime.now()
        while True:
            try:
                return await self.query_tx(tx_hash)
            except NotFoundError:
                pass

            delta = datetime.now() - start
            if delta >= timeout:
                raise QueryTimeoutError()

            await asyncio.sleep(poll_period.total_seconds())

    async def query_tx(self, tx_hash: str) -> TxResponse:
        """query transaction.

        :param tx_hash: transaction hash
        :raises NotFoundError: Tx details not found
        :raises grpc.RpcError: RPC connection issue
        :return: query response
        """
        req = GetTxRequest(hash=tx_hash)
        try:
            resp = await self.txs.GetTx(req)
        except grpc.RpcError as e:
            if self._is_tx_not_found_error(e):
                raise NotFoundError() from e
            raise
        except RuntimeError as e:
            if self._is_tx_not_found_error(e):
                raise NotFoundError() from e
            raise

        return self._parse_tx_response(resp.tx_response)

    async def simulate_tx(self, tx: Transaction) -> int:
        """simulate transaction.

        :param tx: transaction
        :return: gas used in transaction
        """
        self._check_tx_final_for_simulation(tx)

        req = SimulateRequest(tx=tx.tx)
        resp = await self.txs.Simulate(req)

        return int(resp.gas_info.gas_used)

    async def broadcast_tx(self, tx: Transaction) -> AsyncSubmittedTx:
        """Broadcast transaction.

        :param tx: transaction
        :return: Submitted transaction
        """
        # create the broadcast request
        broadcast_req = BroadcastTxRequest(
            tx_bytes=tx.tx.SerializeToString(), mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        # broadcast the transaction
        resp = await self.txs.BroadcastTx(broadcast_req)
        tx_digest = self._check_broadcast_response(resp)

        return AsyncSubmittedTx(self, tx_digest)

    async def query_latest_block(self) -> Block:
        """Query the latest block.

        :return: latest block
        """
        req = GetLatestBlockRequest()
        resp = await self.tendermint.GetLatestBlock(req)
        return Block.from_proto(resp.block)

    async def query_block(self, height: int) -> Block:
        """Query the block.

        :param height: block height
        :return: block
        """
        req = GetBlockByHeightRequest(height=height)
        resp = await self.tendermint.GetBlockByHeight(req)
        return Block.from_proto(resp.block)

    async def query_height(self) -> int:
        """Query the latest block height.

        :return: latest block height
        """
        return (await self.query_latest_block()).height

    async def query_chain_id(self) -> str:
        """Query the chain id.

        :return: chain id
        """
        return (await self.query_latest_block()).chain_id


async def simulate_tx(
    client: AsyncLedgerClient,
    tx: Transaction,
    sender: Wallet,
    account: Optional[Account] = None,
    memo: Optional[str] = None,
) -> Tuple[int, str, Account]:
    """Estimate transaction fees based on either a provided amount, gas limit, or simulation.

    :param client: Async ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param memo: Transaction memo, defaults to None

    :return: Estimated gas_limit and fee amount tuple
    """
    # query the account information for the sender
    if account is None:
        account = await client.query_account(sender.address())

    # we need to build up a representative transaction so that we can accurately simulate it
    tx.seal(
        SigningCfg.direct(sender.public_key(), account.sequence),
        fee=TxFee([], 0),
        memo=memo,
    )
    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    # simulate the gas and fee for the transaction
    gas_limit, fee = await client.estimate_gas_and_fee_for_tx(tx)

    return gas_limit, fee, account


async def prepare_basic_transaction(
    client: AsyncLedgerClient,
    tx: Transaction,
    sender: Wallet,
    account: Optional[Account] = None,
    fee: Optional[TxFee] = None,
    memo: Optional[str] = None,
    timeout_height: Optional[int] = None,
) -> Transaction:
    """Prepare basic transaction.

    :param client: Async ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param fee: The tx fee (see below the behaviour):
                - If the `fee` *or* `fee.gas_limit` is `None`, then the `simulate_tx(...)` will be executed to
                  estimate the `fee.gas_limit` value.
                - If the `fee.amount` is `None` then it will be calculated from the `fee.gas_limit` and `gas_price`
                  values (the `gas_price` value will be taken from client config).
    :param memo: Transaction memo, defaults to None
    :param timeout_height: timeout height, defaults to None

    :return: transaction
    """
    if fee is None:
        fee = TxFee()

    # query the account information for the sender
    if account is None:
        account = await client.query_account(sender.address())

    if fee.gas_limit is None:
        # Simulate transaction to get gas and amount
        fee.gas_limit, estimated_amount, _ = await simulate_tx(
            client, tx, sender, account, memo
        )
        # Use estimated amount if not provided
        fee.amount = fee.amount or estimated_amount  # type: ignore

    if fee.amount is None:
        fee.amount = client.estimate_fee_from_gas(fee.gas_limit)  # type: ignore

    # Build the final transaction
    tx.seal(
        SigningCfg.direct(sender.public_key(), account.sequence),
        fee=fee,
        memo=memo,
        timeout_height=timeout_height,
    )

    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    return tx


async def prepare_and_broadcast_basic_transaction(
    client: AsyncLedgerClient,
    tx: Transaction,
    sender: Wallet,
    account: Optional[Account] = None,
    fee: Optional[TxFee] = None,
    memo: Optional[str] = None,
    timeout_height: Optional[int] = None,
) -> AsyncSubmittedTx:
    """Prepare and broadcast basic transaction.

    :param client: Async ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param fee: The tx fee (see below the behaviour):
                - If the `fee` *or* `fee.gas_limit` is `None`, then the `simulate_tx(...)` will be executed to
                  estimate the `fee.gas_limit` value.
                - If the `fee.amount` is `None` then it will be calculated from the `fee.gas_limit` and `gas_price`
                  values (the `gas_price` value will be taken from client config).
    :param memo: Transaction memo, defaults to None
    :param timeout_height: timeout height, defaults to None

    :return: broadcast transaction
    """
    tx = await prepare_basic_transaction(
        client, tx, sender, account, fee, memo, timeout_height
    )
    return await client.broadcast_tx(tx)


async def get_paginated(
    initial_request: Any,
    request_method: Callable,
    pages_limit: int = 0,
    per_page_limit: Optional[int] = DEFAULT_PER_PAGE_LIMIT,
) -> List[Any]:
    """
    Get pages for specific request.

    :param initial_request: request supports pagination
    :param request_method: async function to perform request
    :param pages_limit: max number of pages to return. default - 0 unlimited
    :param per_page_limit: Optional int: amount of records per one page. default is None, determined by server

    :return: List of responses
    """
    pages: List[Any] = []
    pagination = PageRequest(limit=per_page_limit)

    while pagination and (len(pages) < pages_limit or pages_limit == 0):
        request = initial_request.__class__()
        request.CopyFrom(initial_request)
        request.pagination.CopyFrom(pagination)

        resp = await request_method(request)

        pages.append(resp)

        pagination = None

        if resp.pagination.next_key:
            pagination = PageRequest(limit=per_page_limit, key=resp.pagination.next_key)
    return pages
