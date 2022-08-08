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

"""Osmosis contract test."""
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from tests.integration.osmosis_testnet.net_config import NET_CONFIG, FaucetMixIn
from tests.integration.test_contract import TestContract as BaseTestContract


class DisabledTestContract(BaseTestContract, FaucetMixIn):
    PREFIX = "osmo"

    def get_ledger(self):
        return LedgerClient(NET_CONFIG)

    def get_wallet(self):
        wallet = LocalWallet.generate(prefix=self.PREFIX)
        self._ask_funds(wallet)
        return wallet
