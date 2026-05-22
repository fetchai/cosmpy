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


"""Test aerial ledger client."""


import datetime
from types import SimpleNamespace

from google.protobuf.timestamp_pb2 import Timestamp

from cosmpy.aerial.client import (
    Block,
    DEFAULT_QUERY_INTERVAL_SECS,
    DEFAULT_QUERY_TIMEOUT_SECS,
    LedgerClient,
)
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.grpc.rpc_wrapper import RpcMethodWrapper
from cosmpy.aerial.query_client import is_query_grpc_stub
from cosmpy.aerial.query_context import RequestQueryContext, ResponseQueryContext
from cosmpy.common.rest_client import COSMOS_BLOCK_HEIGHT_HEADER
from cosmpy.protos.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse as PbTxResponse
from cosmpy.protos.tendermint.types.block_pb2 import Block as PbBlock
from cosmpy.protos.tendermint.types.types_pb2 import Data, Header


def test_ledger_client_timeouts():
    """Test ledger client query_interval_secs and query_timeout_secs options."""
    client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    assert (
        client._query_interval_secs  # pylint: disable=protected-access
        == DEFAULT_QUERY_INTERVAL_SECS
    )

    assert (
        client._query_timeout_secs  # pylint: disable=protected-access
        == DEFAULT_QUERY_TIMEOUT_SECS
    )

    timeout = 100
    interval = 5000
    client = LedgerClient(
        NetworkConfig.fetchai_stable_testnet(),
        query_interval_secs=interval,
        query_timeout_secs=timeout,
    )
    assert client._query_interval_secs == interval  # pylint: disable=protected-access
    assert client._query_timeout_secs == timeout  # pylint: disable=protected-access


def test_ledger_client_query_context_is_optional():
    """Test ledger client query context is per call and optional."""
    cfg = NetworkConfig(
        chain_id="test-chain",
        fee_minimum_gas_price=1,
        fee_denomination="atest",
        staking_denomination="atest",
        url="rest+http://localhost:1317",
    )

    client = LedgerClient(cfg)
    original_bank = client.bank

    assert client.network_config == cfg
    assert (
        client._query_interval_secs == DEFAULT_QUERY_INTERVAL_SECS
    )  # pylint: disable=protected-access
    assert (
        client._query_timeout_secs == DEFAULT_QUERY_TIMEOUT_SECS
    )  # pylint: disable=protected-access
    assert client.bank is original_bank


def test_rpc_method_wrapper_merges_metadata_and_reads_response_height():
    """Test gRPC RPC wrapper handles request and response query height."""

    class Rpc:
        """Fake gRPC RPC method."""

        def with_call(self, request, metadata=None, **kwargs):
            self.request = request
            self.metadata = metadata
            self.kwargs = kwargs
            call = SimpleNamespace(
                trailing_metadata=lambda: ((COSMOS_BLOCK_HEIGHT_HEADER, "456"),),
                initial_metadata=lambda: (),
            )
            return "response", call

    rpc = Rpc()
    ctx = RequestQueryContext(request_height=123)

    response = RpcMethodWrapper(rpc)(
        "request",
        ctx=ctx,
        metadata=(("existing", "value"),),
        timeout=1,
    )

    assert response == "response"
    assert rpc.request == "request"
    assert rpc.metadata == [
        ("existing", "value"),
        (COSMOS_BLOCK_HEIGHT_HEADER, "123"),
    ]
    assert rpc.kwargs == {"timeout": 1}
    assert ctx.response_height == 456


def test_rpc_method_wrapper_reads_latest_response_height():
    """Test gRPC RPC wrapper can read response height without request height."""

    class Rpc:
        """Fake gRPC RPC method."""

        @staticmethod
        def with_call(request, metadata=None, **kwargs):
            call = SimpleNamespace(
                trailing_metadata=lambda: (),
                initial_metadata=lambda: ((COSMOS_BLOCK_HEIGHT_HEADER, "789"),),
            )
            return "response", call

    ctx = ResponseQueryContext()
    response = RpcMethodWrapper(Rpc())("request", ctx=ctx)

    assert response == "response"
    assert ctx.response_height == 789


def test_grpc_query_stub_detection():
    """Test only generated query gRPC stubs are detected as query stubs."""

    class QueryStub:
        """Fake generated query stub."""

    class TxServiceStub:
        """Fake generated tx service stub."""

    QueryStub.__module__ = "cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc"
    TxServiceStub.__module__ = "cosmpy.protos.cosmos.tx.v1beta1.service_pb2_grpc"

    assert is_query_grpc_stub(QueryStub())
    assert not is_query_grpc_stub(TxServiceStub())


def test_parsing_tx_response():
    """Test parsing tx response."""
    txhash = "hash"
    height = 123
    code = 456
    gas_wanted = 789
    gas_used = 101112
    raw_log = "raw_log"
    logs = []
    events = {}
    timestamp = "2023-05-09T08:21:03Z"
    timestamp_dt = datetime.datetime(2023, 5, 9, 8, 21, 3, tzinfo=datetime.timezone.utc)
    tx_response = PbTxResponse(
        txhash=txhash,
        height=height,
        code=code,
        gas_wanted=gas_wanted,
        gas_used=gas_used,
        raw_log=raw_log,
        logs=logs,
        events=events,
        timestamp=timestamp,
    )

    tx = LedgerClient._parse_tx_response(tx_response)  # pylint: disable=W0212

    assert tx.hash == txhash
    assert tx.height == height
    assert tx.code == code
    assert tx.gas_wanted == gas_wanted
    assert tx.gas_used == gas_used
    assert tx.raw_log == raw_log
    assert tx.logs == logs
    assert tx.events == events
    assert tx.timestamp == timestamp_dt


def test_parse_block():
    """Test parsing block response."""
    # Test data
    chain_id = "something"
    height = 123
    timestamp = Timestamp(seconds=1234567890, nanos=5678910)
    txs = [b"tx1", b"tx2"]

    # Create block response
    block_header = Header(chain_id=chain_id, height=height, time=timestamp)
    block_data = Data(txs=txs)
    pb_block = PbBlock(header=block_header, data=block_data)

    # Parse block by height response
    block = Block.from_proto(pb_block)

    # Check results
    assert block.height == height
    assert block.time == datetime.datetime(
        2009, 2, 13, 23, 31, 30, tzinfo=datetime.timezone.utc, microsecond=5678
    )
    assert block.tx_hashes == [
        "709B55BD3DA0F5A838125BD0EE20C5BFDD7CABA173912D4281CAE816B79A201B",
        "27CA64C092A959C7EDC525ED45E845B1DE6A7590D173FD2FAD9133C8A779A1E3",
    ]
    assert block.chain_id == chain_id
