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

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract_path", help="The path to the contract to upload")
    parser.add_argument(
        "contract_address",
        nargs="?",
        type=Address,
        help="The address of the contract is already deployed",
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
    contract.deploy({}, wallet)

    print(f"Contract deployed at: {contract.address}")

    result = contract.query({"get": {"owner": wallet}})
    print("Initial state:", result)

    contract.execute({"set": {"value": "foobar"}}, wallet).wait_to_complete()

    result = contract.query({"get": {"owner": wallet}})
    print("State after set:", result)

    contract.execute({"clear": {}}, wallet).wait_to_complete()

    result = contract.query({"get": {"owner": wallet}})
    print("State after clear:", result)


if __name__ == "__main__":
    main()
