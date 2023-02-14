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

"""Osmosis network config."""
from time import sleep

import requests

from cosmpy.aerial.config import NetworkConfig

NET_CONFIG = NetworkConfig(
    chain_id="osmo-test-4",
    url="grpc+http://grpc-test.osmosis.zone:443/",
    fee_minimum_gas_price=1,
    fee_denomination="uosmo",
    staking_denomination="uosmo",
)


class FaucetMixIn:
    """Osmosis faucet config"""

    def ask_funds(self, wallet):
        """Request fund from faucet.

        :param wallet: Wallet Address
        :raises Exception: fail to topup
        """
        resp = requests.post(
            "https://testnet-faucet.dev-osmosis.zone/request",
            json={"address": str(wallet.address())},
        )
        assert resp.status_code == 200
        ledger = self.get_ledger()
        for i in range(10):
            if ledger.query_bank_balance(wallet.address()) > 0:
                break
            sleep(i * 2)
        else:
            raise Exception("fail to topup")
