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

from cosmpy.aerial.gas import (
    GasStrategy,
    OfflineMessageTableStrategy,
    SimulationGasStrategy,
)
from cosmpy.aerial.tx import Transaction
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmwasm.wasm.v1.tx_pb2 import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgStoreCode,
)


@pytest.mark.parametrize(
    "input_msgs,expected_gas_estimate",
    [
        ([MsgSend()], 100_000),
        ([MsgStoreCode()], 2_000_000),
        ([MsgInstantiateContract()], 250_000),
        ([MsgExecuteContract()], 400_000),
        ([MsgSend(), MsgSend()], 200_000),
        ([MsgSend(), MsgStoreCode()], 2_000_000),  # hits block limit
        ([MsgSend(), MsgInstantiateContract()], 350_000),
        ([MsgInstantiateContract(), MsgExecuteContract()], 650_000),
    ],
)
def test_table_gas_estimation(input_msgs, expected_gas_estimate):
    # build up the TX
    tx = Transaction()
    for input_msg in input_msgs:
        tx.add_message(input_msg)

    # estimate the gas for this test transaction
    strategy: GasStrategy = OfflineMessageTableStrategy.default_table()
    gas_estimate = strategy.estimate_gas(tx)

    assert gas_estimate == expected_gas_estimate


class MockLedger:
    def __init__(self):
        self._table = OfflineMessageTableStrategy.default_table()

    def simulate_tx(self, tx: Transaction) -> int:
        return self._table.estimate_gas(tx)

    def query_params(self, subspace: str, key: str) -> Any:
        return {"max_gas": -1}


@pytest.mark.parametrize(
    "input_msgs,expected_gas_estimate",
    [
        ([MsgSend()], 100_000),
        ([MsgStoreCode()], 2_000_000),
        ([MsgInstantiateContract()], 250_000),
        ([MsgExecuteContract()], 400_000),
        ([MsgSend(), MsgSend()], 200_000),
        ([MsgSend(), MsgStoreCode()], 2_000_000),  # hits block limit
        ([MsgSend(), MsgInstantiateContract()], 350_000),
        ([MsgInstantiateContract(), MsgExecuteContract()], 650_000),
    ],
)
def test_simulated_estimation(input_msgs, expected_gas_estimate):
    ledger = MockLedger()
    strategy = SimulationGasStrategy(ledger, 1.0)

    # build up the TX
    tx = Transaction()
    for input_msg in input_msgs:
        tx.add_message(input_msg)

    gas_estimate = strategy.estimate_gas(tx)

    assert gas_estimate == expected_gas_estimate
