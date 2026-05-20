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
    GrpcHeightInterceptor,
    LedgerClient,
    _is_query_grpc_stub,
)
from cosmpy.aerial.config import NetworkConfig
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


def test_ledger_client_with_height_is_isolated():
    """Test ledger client can create an isolated query height context."""
    cfg = NetworkConfig(
        chain_id="test-chain",
        fee_minimum_gas_price=1,
        fee_denomination="atest",
        staking_denomination="atest",
        url="rest+http://localhost:1317",
    )

    client = LedgerClient(cfg)
    assert client.bank._rest_api._height() is None  # pylint: disable=protected-access
    original_bank = client.bank

    with client.with_height(123) as height_client:
        assert height_client is client
        assert height_client.network_config == cfg
        assert height_client._query_interval_secs == client._query_interval_secs  # pylint: disable=protected-access
        assert height_client._query_timeout_secs == client._query_timeout_secs  # pylint: disable=protected-access
        assert height_client.bank._rest_api._height() == 123  # pylint: disable=protected-access
        assert height_client.bank is original_bank

        with height_client.with_height(456) as nested_client:
            assert nested_client is client
            assert nested_client.bank._rest_api._height() == 456  # pylint: disable=protected-access

        assert height_client.bank._rest_api._height() == 123  # pylint: disable=protected-access

    assert client.bank._rest_api._height() is None  # pylint: disable=protected-access
    assert client.bank is original_bank

    with client.with_height(None) as latest_client:
        assert latest_client is client
        assert latest_client.bank._rest_api._height() is None  # pylint: disable=protected-access


def test_grpc_height_interceptor_merges_metadata():
    """Test gRPC height interceptor appends Cosmos block height metadata."""
    interceptor = GrpcHeightInterceptor(lambda: 123)
    call_details = SimpleNamespace(
        method="/test.Service/Query",
        timeout=1,
        metadata=(("existing", "value"),),
        credentials=None,
        wait_for_ready=None,
        compression=None,
    )

    def continuation(next_call_details, request):
        return next_call_details, request

    next_call_details, request = interceptor.intercept_unary_unary(
        continuation, call_details, "request"
    )

    assert request == "request"
    assert next_call_details.metadata == (
        ("existing", "value"),
        (COSMOS_BLOCK_HEIGHT_HEADER, "123"),
    )


def test_grpc_query_stub_detection():
    """Test only generated query gRPC stubs are detected as query stubs."""

    class QueryStub:
        """Fake generated query stub."""

    class TxServiceStub:
        """Fake generated tx service stub."""

    QueryStub.__module__ = "cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc"
    TxServiceStub.__module__ = "cosmpy.protos.cosmos.tx.v1beta1.service_pb2_grpc"

    assert _is_query_grpc_stub(QueryStub)
    assert not _is_query_grpc_stub(TxServiceStub)


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
