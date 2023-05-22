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

from google.protobuf.timestamp_pb2 import Timestamp

from cosmpy.aerial.client import (
    DEFAULT_QUERY_INTERVAL_SECS,
    DEFAULT_QUERY_TIMEOUT_SECS,
    LedgerClient,
)
from cosmpy.aerial.config import NetworkConfig
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
    timestamp = Timestamp(seconds=1234567890)
    txs = [b"tx1", b"tx2"]

    # Create block response
    block_header = Header(chain_id=chain_id, height=height, time=timestamp)
    block_data = Data(txs=txs)
    pb_block = PbBlock(header=block_header, data=block_data)

    # Parse block by height response
    block = LedgerClient._parse_block(pb_block)  # pylint: disable=W0212

    # Check results
    assert block.height == height
    assert block.time == datetime.datetime(
        2009, 2, 13, 23, 31, 30, tzinfo=datetime.timezone.utc
    )
    assert block.tx_hashes == [
        "709B55BD3DA0F5A838125BD0EE20C5BFDD7CABA173912D4281CAE816B79A201B",
        "27CA64C092A959C7EDC525ED45E845B1DE6A7590D173FD2FAD9133C8A779A1E3",
    ]
    assert block.chain_id == chain_id
