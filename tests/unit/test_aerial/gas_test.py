"""Test for gas."""

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
from typing import Any

import pytest

from c4epy.aerial.gas import (
    GasStrategy,
    OfflineMessageTableStrategy,
    SimulationGasStrategy,
)
from c4epy.aerial.tx import Transaction
from c4epy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend


@pytest.mark.parametrize(
    "input_msgs,expected_gas_estimate",
    [
        ([MsgSend()], 100_000),
        ([MsgSend(), MsgSend()], 200_000),
    ],
)
def test_table_gas_estimation(input_msgs, expected_gas_estimate):
    """Test estimated gas for transaction."""
    # build up the TX
    tx = Transaction()
    for input_msg in input_msgs:
        tx.add_message(input_msg)

    # estimate the gas for this test transaction
    strategy: GasStrategy = OfflineMessageTableStrategy.default_table()
    gas_estimate = strategy.estimate_gas(tx)

    assert gas_estimate == expected_gas_estimate


class MockLedger:
    """Test for ledger."""

    def __init__(self):
        """Initiate Mock Ledger with table."""
        self._table = OfflineMessageTableStrategy.default_table()

    def simulate_tx(self, tx: Transaction) -> int:
        """Simulate tx."""
        return self._table.estimate_gas(tx)

    def query_params(
        self, subspace: str, key: str  # pylint: disable=unused-argument
    ) -> Any:
        """Set query params."""
        return {"max_gas": -1}


@pytest.mark.parametrize(
    "input_msgs,expected_gas_estimate",
    [
        ([MsgSend()], 100_000),
        ([MsgSend(), MsgSend()], 200_000),
    ],
)
def test_simulated_estimation(input_msgs, expected_gas_estimate):
    """Test simulated estimation of gas for transaction."""
    ledger = MockLedger()
    strategy = SimulationGasStrategy(ledger, 1.0)

    # build up the TX
    tx = Transaction()
    for input_msg in input_msgs:
        tx.add_message(input_msg)

    gas_estimate = strategy.estimate_gas(tx)

    assert gas_estimate == expected_gas_estimate
