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

"""Theta tx test."""

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from tests.integration.cosmos_theta_testnet.net_config import THETA_NET_CONFIG
from tests.integration.test_tx import TestTx as BaseTestTx


class TestTx(BaseTestTx):
    COIN = "uatom"
    GAS_LIMIT = 120000

    def get_wallet_1(self):
        prefix = "cosmos"
        return LocalWallet(
            PrivateKey("L1GsisFk+oaIug3XZlILWk2pJDVFS5aPJsrovvUEDrE="), prefix=prefix
        )

    def get_wallet_2(self):
        return LocalWallet.generate(prefix="cosmos")

    def get_ledger(self):
        return LedgerClient(THETA_NET_CONFIG)