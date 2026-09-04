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


"""Test aerial async ledger client."""


import asyncio
from dataclasses import replace
from types import SimpleNamespace

import pytest
from google.protobuf.any_pb2 import Any as ProtoAny

from cosmpy.aerial.client import (
    DEFAULT_QUERY_INTERVAL_SECS,
    DEFAULT_QUERY_TIMEOUT_SECS,
    LedgerClient,
)
from cosmpy.aerial.client.aio import AsyncLedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.exceptions import NotFoundError, QueryTimeoutError
from cosmpy.aerial.gas import AsyncSimulationGasStrategy, OfflineMessageTableStrategy
from cosmpy.aerial.grpc.rpc_wrapper import AsyncRpcMethodWrapper
from cosmpy.aerial.grpc.stub_wrapper import AsyncStubWrapper
from cosmpy.aerial.query_client import AsyncNoopQueryClientWrapper
from cosmpy.aerial.query_context import RequestQueryContext, ResponseQueryContext
from cosmpy.aerial.tx_helpers import AsyncSubmittedTx
from cosmpy.common.rest_client import COSMOS_BLOCK_HEIGHT_HEADER
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountResponse
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceResponse
from cosmpy.protos.cosmos.base.abci.v1beta1.abci_pb2 import GasInfo
from cosmpy.protos.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse as PbTxResponse
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as PbCoin
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import (
    BroadcastTxResponse,
    GetTxResponse,
    SimulateResponse,
)


TEST_ADDRESS = Address("fetch12hyw0z8za0sc9wwfhkdz2qrc89a87z42py23vn")


def run_with_client(coro_fn, **client_kwargs):
    """Run coro_fn(client) inside a fresh event loop.

    The grpc.aio channel must be created from within a running event loop, so the
    client is constructed inside the loop, mirroring real-world usage with
    ``asyncio.run(main())``.

    :param coro_fn: async callable taking the client as its only argument
    :param client_kwargs: extra kwargs for the AsyncLedgerClient constructor
    :return: result of coro_fn
    """

    async def main():
        async with AsyncLedgerClient(
            NetworkConfig.fetchai_stable_testnet(), **client_kwargs
        ) as client:
            return await coro_fn(client)

    return asyncio.run(main())


def test_async_ledger_client_timeouts():
    """Test async ledger client query_interval_secs and query_timeout_secs options."""

    async def check_defaults(client):
        assert (
            client._query_interval_secs  # pylint: disable=protected-access
            == DEFAULT_QUERY_INTERVAL_SECS
        )
        assert (
            client._query_timeout_secs  # pylint: disable=protected-access
            == DEFAULT_QUERY_TIMEOUT_SECS
        )

    run_with_client(check_defaults)

    timeout = 100
    interval = 5000

    async def check_custom(client):
        assert (
            client._query_interval_secs == interval  # pylint: disable=protected-access
        )
        assert client._query_timeout_secs == timeout  # pylint: disable=protected-access

    run_with_client(
        check_custom, query_interval_secs=interval, query_timeout_secs=timeout
    )


def test_async_ledger_client_rejects_rest_endpoints():
    """Test async ledger client raises on REST network configurations."""
    cfg = replace(
        NetworkConfig.fetchai_stable_testnet(),
        url="rest+https://rest-fetchhub.fetch.ai",
    )
    with pytest.raises(RuntimeError, match="gRPC endpoints only"):
        AsyncLedgerClient(cfg)


def test_async_rpc_method_wrapper_merges_metadata_and_reads_response_height():
    """Test async gRPC RPC wrapper handles request and response query height."""

    class Call:
        """Fake async gRPC call."""

        def __init__(self):
            self._response = "response"

        def __await__(self):
            async def _return():
                return self._response

            return _return().__await__()

        async def trailing_metadata(self):
            return ((COSMOS_BLOCK_HEIGHT_HEADER, "456"),)

        async def initial_metadata(self):
            return ()

    class Rpc:
        """Fake async gRPC RPC method."""

        def __call__(self, request, metadata=None, **kwargs):
            self.request = request
            self.metadata = metadata
            self.kwargs = kwargs
            return Call()

    rpc = Rpc()
    ctx = RequestQueryContext(request_height=123)

    response = asyncio.run(
        AsyncRpcMethodWrapper(rpc)(
            "request",
            ctx=ctx,
            metadata=(("existing", "value"),),
            timeout=1,
        )
    )

    assert response == "response"
    assert rpc.request == "request"
    assert rpc.metadata == [
        ("existing", "value"),
        (COSMOS_BLOCK_HEIGHT_HEADER, "123"),
    ]
    assert rpc.kwargs == {"timeout": 1}
    assert ctx.response_height == 456


def test_async_rpc_method_wrapper_reads_latest_response_height():
    """Test async gRPC RPC wrapper can read response height without request height."""

    class Call:
        """Fake async gRPC call."""

        def __await__(self):
            async def _return():
                return "response"

            return _return().__await__()

        async def trailing_metadata(self):
            return ()

        async def initial_metadata(self):
            return ((COSMOS_BLOCK_HEIGHT_HEADER, "789"),)

    class Rpc:
        """Fake async gRPC RPC method."""

        @staticmethod
        def __call__(request, metadata=None, **kwargs):
            return Call()

    ctx = ResponseQueryContext()
    response = asyncio.run(AsyncRpcMethodWrapper(Rpc())("request", ctx=ctx))

    assert response == "response"
    assert ctx.response_height == 789


def test_async_ledger_client_wraps_query_stubs():
    """Test async ledger client wraps query stubs for query context support."""

    async def check(client):
        assert isinstance(client.bank, AsyncStubWrapper)
        assert isinstance(client.auth, AsyncStubWrapper)
        assert isinstance(client.tendermint, AsyncStubWrapper)
        assert isinstance(client.txs, AsyncNoopQueryClientWrapper)

    run_with_client(check)


def test_async_query_account():
    """Test querying an account over a mocked async auth stub."""
    account = BaseAccount(address=str(TEST_ADDRESS), account_number=5, sequence=7)
    packed_account = ProtoAny()
    packed_account.Pack(account)

    class MockAuthStub:  # pylint: disable=too-few-public-methods
        """Mock async auth stub."""

        async def Account(
            self, request, ctx=None
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Return a fixed account query response."""
            return QueryAccountResponse(account=packed_account)

    async def check(client):
        client.auth = MockAuthStub()
        return await client.query_account(TEST_ADDRESS)

    result = run_with_client(check)
    assert result.address == TEST_ADDRESS
    assert result.number == 5
    assert result.sequence == 7


def test_async_query_bank_balance_with_query_context():
    """Test querying a bank balance forwards query context to the stub."""

    class MockBankStub:  # pylint: disable=too-few-public-methods
        """Mock async bank stub."""

        def __init__(self):
            self.ctx = None

        async def Balance(
            self, request, ctx=None
        ):  # noqa: N802 # pylint: disable=invalid-name
            """Return a fixed balance and capture the query context."""
            self.ctx = ctx
            if ctx is not None:
                ctx.response_height = 42
            return QueryBalanceResponse(
                balance=PbCoin(denom=request.denom, amount="1234")
            )

    async def check(client):
        stub = MockBankStub()
        client.bank = stub
        ctx = ResponseQueryContext()
        balance = await client.query_bank_balance(TEST_ADDRESS, ctx=ctx)
        return balance, ctx.response_height, stub.ctx

    balance, response_height, forwarded_ctx = run_with_client(check)
    assert balance == 1234
    assert response_height == 42
    assert forwarded_ctx is not None


def test_async_query_tx_not_found_and_wait_timeout():
    """Test tx not found translation and wait_for_query_tx timeout."""

    class MockTxStub:  # pylint: disable=too-few-public-methods
        """Mock async tx stub whose GetTx always fails with 'tx not found'."""

        async def GetTx(
            self, request, ctx=None
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Raise a 'tx not found' error."""
            raise RuntimeError("tx not found")

    async def check_not_found(client):
        client.txs = MockTxStub()
        await client.query_tx("DEADBEEF")

    with pytest.raises(NotFoundError):
        run_with_client(check_not_found)

    async def check_timeout(client):
        client.txs = MockTxStub()
        await client.wait_for_query_tx("DEADBEEF", timeout=0.2, poll_period=0.05)

    with pytest.raises(QueryTimeoutError):
        run_with_client(check_timeout)


def test_async_broadcast_and_wait():
    """Test broadcasting a transaction and waiting for its completion."""
    tx_hash = "ABCDEF0123456789"

    class MockTxStub:  # pylint: disable=too-few-public-methods
        """Mock async tx stub for broadcast and completion polling."""

        async def BroadcastTx(
            self, request
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Return a successful broadcast response."""
            return BroadcastTxResponse(tx_response=PbTxResponse(txhash=tx_hash, code=0))

        async def GetTx(
            self, request, ctx=None
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Return a completed tx response."""
            return GetTxResponse(
                tx_response=PbTxResponse(txhash=tx_hash, code=0, height=42)
            )

    tx = SimpleNamespace(tx=SimpleNamespace(SerializeToString=lambda: b""))

    async def check(client):
        client.txs = MockTxStub()
        submitted = await client.broadcast_tx(tx)
        assert isinstance(submitted, AsyncSubmittedTx)
        assert submitted.tx_hash == tx_hash
        return await submitted.wait_to_complete(timeout=1, poll_period=0.05)

    submitted = run_with_client(check)
    assert submitted.response is not None
    assert submitted.response.height == 42


def test_async_gas_estimation_with_simulation_strategy():
    """Test the async simulation gas strategy end to end over mocked stubs."""

    class MockTxStub:  # pylint: disable=too-few-public-methods
        """Mock async tx stub for gas simulation."""

        async def Simulate(
            self, request
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Return a fixed gas-used simulation response."""
            return SimulateResponse(gas_info=GasInfo(gas_used=100_000))

    class MockConsensusStub:  # pylint: disable=too-few-public-methods
        """Mock async consensus stub."""

        async def Params(
            self, request, ctx=None
        ):  # noqa: N802 # pylint: disable=invalid-name,unused-argument
            """Return consensus params with a fixed block max_gas."""
            return SimpleNamespace(
                params=SimpleNamespace(block=SimpleNamespace(max_gas=3_000_000))
            )

    tx = SimpleNamespace(state="unused", tx=None)

    async def check(client):
        client.txs = MockTxStub()
        client.consensus = MockConsensusStub()
        assert isinstance(client.gas_strategy, AsyncSimulationGasStrategy)
        # bypass the final-state check by using a transaction-like object
        client._check_tx_final_for_simulation = (  # pylint: disable=protected-access
            lambda _tx: None
        )
        return await client.estimate_gas_and_fee_for_tx(tx)

    gas, fee = run_with_client(check)
    assert gas == int(100_000 * AsyncSimulationGasStrategy.DEFAULT_MULTIPLIER)
    assert fee.endswith(NetworkConfig.fetchai_stable_testnet().fee_denomination)


def test_async_client_accepts_sync_offline_gas_strategy():
    """Test that an I/O-free sync gas strategy can be used by the async client."""
    tx = SimpleNamespace(msgs=[])

    async def check(client):
        client.gas_strategy = OfflineMessageTableStrategy.default_table()
        return await client.estimate_gas_for_tx(tx)

    assert run_with_client(check) == 0


def test_sync_and_async_clients_share_parsing():
    """Test both clients share the same tx-response parsing implementation."""
    assert (
        LedgerClient._parse_tx_response  # pylint: disable=protected-access
        is AsyncLedgerClient._parse_tx_response  # pylint: disable=protected-access
    )
