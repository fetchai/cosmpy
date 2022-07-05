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
"""Integration tests for basic transactions."""
import pytest

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet


@pytest.mark.integration
def test_faucet_transaction_balance():
    """Test faucet claims, tx settled, balance check."""
    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())
    wallet1 = LocalWallet.generate()
    wallet2 = LocalWallet.generate()

    balance1 = ledger.query_bank_balance(wallet1.address())

    faucet_api.get_wealth(wallet1.address())
    balance2 = ledger.query_bank_balance(wallet1.address())

    assert balance2 > balance1

    wallet2_balance1 = ledger.query_bank_balance(wallet2.address())
    tokens_to_send = int(balance2 / 2)
    tx = ledger.send_tokens(wallet2.address(), tokens_to_send, "atestfet", wallet1)
    tx.wait_to_complete()
    wallet2_balance2 = ledger.query_bank_balance(wallet2.address())
    assert wallet2_balance2 == wallet2_balance1 + tokens_to_send


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
