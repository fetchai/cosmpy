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
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey


def main():
    alice_private_key = PrivateKey("T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s=")
    bob_private_key = PrivateKey("CI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")

    alice_address = Address(alice_private_key)
    bob_address = Address(bob_private_key)

    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    print(
        f"Alice Address: {alice_address} Balance: {ledger.query_bank_balance(alice_address)}"
    )
    print(
        f"Bob   Address: {bob_address} Balance: {ledger.query_bank_balance(bob_address)}"
    )

    tx = ledger.send_tokens(bob_address, 10, "atestfet", alice_private_key)

    print(f"TX {tx.tx_hash} waiting to complete...")
    tx.wait_to_complete()
    print(f"TX {tx.tx_hash} waiting to complete...done")

    print(
        f"Alice Address: {alice_address} Balance: {ledger.query_bank_balance(alice_address)}"
    )
    print(
        f"Bob   Address: {bob_address} Balance: {ledger.query_bank_balance(bob_address)}"
    )


if __name__ == "__main__":
    main()
