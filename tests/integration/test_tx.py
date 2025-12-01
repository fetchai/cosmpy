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
from cosmpy.aerial.wallet import LocalWallet


MAX_FLAKY_RERUNS = 3
RERUNS_DELAY = 10
VALIDATOR_MNEMONIC = "boat leave enrich glare into second this model appear owner strong tail perfect fringe best still soup clap betray rigid bleak return minimum goddess"


class TestTx:
    """Test Basic Transaction"""

    COIN = "atestfet"

    def get_funds(self, wallet: LocalWallet):
        """Send funds from validator wallet to given wallet."""
        ledger = self.get_ledger()
        validator_walet = self.get_validator_wallet()
        ledger.send_tokens(
            wallet,
            10 * 10**18,
            ledger.network_config.fee_denomination,
            validator_walet,
        ).wait_to_complete()

    def _get_network_config(self):
        """Get network config."""
        local_config = NetworkConfig(
            chain_id="localnet",
            url="grpc+http://127.0.0.1:9090",
            fee_minimum_gas_price=0,
            fee_denomination=self.COIN,
            staking_denomination=self.COIN,
            faucet_url=None,
        )
        return local_config

    def get_validator_wallet(self):
        """Get validator wallet"""
        wallet = LocalWallet.from_mnemonic(VALIDATOR_MNEMONIC)
        return wallet

    def get_wallet(self):
        """Get wallet"""
        wallet = LocalWallet.generate()
        self.get_funds(wallet)
        return wallet

    def get_wallet_1(self):
        """Get wallet 1."""
        wallet1 = LocalWallet.generate()
        self.get_funds(wallet1)
        return wallet1

    def get_wallet_2(self):
        """Get wallet 2."""
        wallet2 = LocalWallet.generate()
        return wallet2

    def get_ledger(self):
        """Get ledger"""
        return LedgerClient(self._get_network_config())

    @pytest.mark.integration
    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS, reruns_delay=RERUNS_DELAY)
    def test_faucet_transaction_balance(self):
        """Test faucet claims, tx settled, balance check."""
        ledger = self.get_ledger()
        wallet1 = self.get_wallet_1()
        wallet2 = self.get_wallet_2()

        wallet1_initial_balance = ledger.query_bank_balance(wallet1.address())
        wallet2_balance1 = ledger.query_bank_balance(wallet2.address())
        block_height = ledger.query_latest_block().height
        tokens_to_send = int(10)
        assert wallet1_initial_balance >= tokens_to_send
        tx = ledger.send_tokens(
            wallet2.address(),
            tokens_to_send,
            self.COIN,
            wallet1,
            timeout_height=block_height + 10,
        )
        tx.wait_to_complete()
        wallet2_balance2 = ledger.query_bank_balance(wallet2.address())
        assert wallet2_balance2 == wallet2_balance1 + tokens_to_send
        wallet1_balance = ledger.query_bank_balance(wallet1.address())
        assert wallet1_balance < wallet1_initial_balance


class TestTxRestAPI(TestTx):
    """Test rest api"""

    def _get_network_config(self):
        denom = "atestfet"
        return NetworkConfig(
            chain_id="localnet",
            url="rest+http://127.0.0.1:1317",
            fee_minimum_gas_price=0,
            fee_denomination=denom,
            staking_denomination=denom,
            faucet_url=None,
        )


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
