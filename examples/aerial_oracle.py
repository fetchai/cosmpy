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
import argparse
from time import sleep

import requests

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address

COIN_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=fetch-ai&vs_currencies=usd"
)
UPDATE_INTERVAL_SECONDS = 10
ORACLE_VALUE_DECIMALS = 5


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "contract_path", help="The path to the oracle contract to upload"
    )
    parser.add_argument(
        "contract_address",
        nargs="?",
        type=Address,
        help="The address of the oracle contract if already deployed",
    )
    return parser.parse_args()


def main():
    args = _parse_commandline()

    wallet = LocalWallet.generate()

    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    wallet_balance = ledger.query_bank_balance(wallet.address())

    while wallet_balance < (10**18):
        print("Providing wealth to wallet...")
        faucet_api.get_wealth(wallet.address())
        wallet_balance = ledger.query_bank_balance(wallet.address())

    contract = LedgerContract(args.contract_path, ledger, address=args.contract_address)

    if not args.contract_address:
        instantiation_message = {"fee": "100"}
        contract.deploy(instantiation_message, wallet, funds="1atestfet")

    print(f"Oracle contract deployed at: {contract.address}")

    grant_role_message = {"grant_oracle_role": {"address": wallet}}
    contract.execute(grant_role_message, wallet).wait_to_complete()

    print(f"Oracle role granted to address: {wallet}")

    while True:
        resp = requests.get(COIN_PRICE_URL).json()
        price = resp["fetch-ai"]["usd"]
        value = int(price * 10**ORACLE_VALUE_DECIMALS)

        update_message = {
            "update_oracle_value": {
                "value": str(value),
                "decimals": str(ORACLE_VALUE_DECIMALS),
            }
        }
        contract.execute(update_message, wallet).wait_to_complete()

        print(f"Oracle value updated to: {price} USD")
        print(f"Next update in {UPDATE_INTERVAL_SECONDS} seconds...")
        sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
