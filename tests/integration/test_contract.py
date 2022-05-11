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
"""Integration tests for contract functions."""
from pathlib import Path

import pytest

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.wallet import LocalWallet
from tests.integration.utils import TestNetFaucetApi

CONTRACT_PATH = Path(__file__).parent / "../../contracts/simple.wasm"


def test_contract():
    """Test simple contract deploy execute and query."""
    wallet = LocalWallet.generate()
    TestNetFaucetApi.get_wealth(wallet.address())
    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())
    contract = LedgerContract(CONTRACT_PATH, ledger)
    contract_address = contract.deploy({}, wallet)
    assert contract_address
    result = contract.query({"get": {"owner": str(wallet.address())}})

    assert not result["exists"]
    assert not result["value"]

    value = "foobar"
    contract.execute({"set": {"value": value}}, wallet).wait_to_complete()
    result = contract.query({"get": {"owner": str(wallet.address())}})

    assert result["exists"]
    assert result["value"] == value


if __name__ == "__main__":
    pytest.main([__file__])
