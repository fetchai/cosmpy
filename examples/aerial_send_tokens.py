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
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet


def main():
    alice = LocalWallet.generate()
    bob = LocalWallet.generate()

    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    alice_balance = ledger.query_bank_balance(bob.address())

    while alice_balance < (10**18):
        print("Providing wealth to alice...")
        faucet_api.get_wealth(alice.address())
        alice_balance = ledger.query_bank_balance(alice.address())

    print(
        f"Alice Address: {alice.address()} Balance: {ledger.query_bank_balance(alice.address())}"
    )
    print(
        f"Bob   Address: {bob.address()} Balance: {ledger.query_bank_balance(bob.address())}"
    )

    tx = ledger.send_tokens(bob.address(), 10, "atestfet", alice)

    print(f"TX {tx.tx_hash} waiting to complete...")
    tx.wait_to_complete()
    print(f"TX {tx.tx_hash} waiting to complete...done")

    print(
        f"Alice Address: {alice.address()} Balance: {ledger.query_bank_balance(alice.address())}"
    )
    print(
        f"Bob   Address: {bob.address()} Balance: {ledger.query_bank_balance(bob.address())}"
    )


if __name__ == "__main__":
    main()
