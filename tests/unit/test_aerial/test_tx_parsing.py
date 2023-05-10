"""Test parsing tx response."""

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
import datetime

from cosmpy.aerial.client import LedgerClient
from cosmpy.protos.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse as PbTxResponse


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

    tx = LedgerClient._parse_tx_response(tx_response)

    assert tx.hash == txhash
    assert tx.height == height
    assert tx.code == code
    assert tx.gas_wanted == gas_wanted
    assert tx.gas_used == gas_used
    assert tx.raw_log == raw_log
    assert tx.logs == logs
    assert tx.events == events
    assert tx.timestamp == timestamp_dt
