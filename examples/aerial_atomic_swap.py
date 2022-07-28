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
from cosmpy.aerial.contract import LedgerContract, create_cosmwasm_execute_msg
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.tx import SigningCfg, Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address

TOKEN_ID_1 = "680564733841876926926749214863536422912"
TOKEN_ID_2 = "680564733841876926926749214863536422913"


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract_path", help="The path to the cosmwasm 1155 contract")
    parser.add_argument(
        "contract_address",
        nargs="?",
        type=Address,
        help="The address of the contract is already deployed",
    )
    return parser.parse_args()


def main():
    args = _parse_commandline()

    alice = LocalWallet.generate()
    bob = LocalWallet.generate()

    client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    # check to see if all the clients have enough funds
    alice_balance = client.query_bank_balance(alice.address())
    bob_balance = client.query_bank_balance(bob.address())
    print(f"Alice balance {alice_balance}")
    print(f"Bob   balance {bob_balance}")

    while alice_balance < (10**18):
        print("Providing wealth to alice...")
        faucet_api.get_wealth(alice.address())
        alice_balance = client.query_bank_balance(alice.address())

    while bob_balance < (10**18):
        print("Providing wealth to bob...")
        faucet_api.get_wealth(bob.address())
        bob_balance = client.query_bank_balance(bob.address())

    contract = LedgerContract(args.contract_path, client, address=args.contract_address)

    # Step 1. Deploy the contract and setup the initial balances as required
    if contract.address is None:
        print("Deploying contract...")
        contract.deploy({}, alice)
        print(f"Contract deployed at {contract.address}")

        create_batch_msg = {
            "create_batch": {
                "item_owner": alice,
                "tokens": [
                    {
                        "id": TOKEN_ID_1,
                        "path": "some_path",
                    },
                    {
                        "id": TOKEN_ID_2,
                        "path": "some_path",
                    },
                ],
            }
        }

        print("Creating tokens...")
        tx = contract.execute(create_batch_msg, alice).wait_to_complete()
        print(f"Created tokens (tx: {tx.tx_hash})")

        # Create Alice's token
        mint_single_msg = {
            "mint_single": {
                "to_address": alice,
                "id": TOKEN_ID_1,
                "supply": "2000",
                "data": "some_data",
            },
        }

        print(f"Minting tokens (id: {TOKEN_ID_1})...")
        tx = contract.execute(mint_single_msg, alice).wait_to_complete()
        print(f"Minted tokens (id: {TOKEN_ID_1} tx: {tx.tx_hash})")

        # Create Bob's token
        mint_single_msg = {
            "mint_single": {
                "to_address": bob.address(),
                "id": TOKEN_ID_2,
                "supply": "2000",
                "data": "some_data",
            },
        }

        print(f"Minting tokens (id: {TOKEN_ID_1})...")
        tx = contract.execute(mint_single_msg, alice).wait_to_complete()
        print(f"Minted tokens (id: {TOKEN_ID_1} tx: {tx.tx_hash})")

    # Step 2. Query what the current balance state is
    result = contract.query(
        {
            "balance_batch": {
                "addresses": [
                    {
                        "address": bob,
                        "id": TOKEN_ID_1,
                    },
                    {
                        "address": alice,
                        "id": TOKEN_ID_2,
                    },
                ]
            }
        }
    )
    print(f'Alice has {result["balances"][1]} of Bob\'s tokens')
    print(f'Bob has {result["balances"][0]} of Alice\'s tokens')

    # Step 3. Perform the atomic swap using the transaction builder and the client

    # Perform an atomic swap. Since this is a specialised operation we need to be able to manually
    # build up the contents of the transaction
    tx = Transaction()

    # add the first message which is instructing the transfer of Alice's token to Bob
    tx.add_message(
        create_cosmwasm_execute_msg(
            alice.address(),
            contract.address,
            {
                "transfer_single": {
                    "operator": alice,
                    "from_address": alice,
                    "to_address": bob,
                    "id": TOKEN_ID_1,
                    "value": "1",
                },
            },
        )
    )

    # add the second message which is instructing the transfer of Bob's token to Alice
    tx.add_message(
        create_cosmwasm_execute_msg(
            bob.address(),
            contract.address,
            {
                "transfer_single": {
                    "operator": bob,
                    "from_address": bob,
                    "to_address": alice,
                    "id": TOKEN_ID_2,
                    "value": "1",
                },
            },
        )
    )

    # lookup the account information for each for Alice and Bob
    alice_account = client.query_account(alice.address())
    bob_account = client.query_account(bob.address())

    # gas and fee estimation
    gas_limit = 300000
    fee = client.estimate_fee_from_gas(gas_limit)

    # seal the transaction: this stops all further updates to the transactions and this is the step
    # where additional metadata is added like gas, fees and the individual signers sequence numbers
    tx.seal(
        [
            SigningCfg.direct(alice.public_key(), alice_account.sequence),
            SigningCfg.direct(bob.public_key(), bob_account.sequence),
        ],
        fee,
        gas_limit,
    )

    # both Alice and Bob sign the transaction
    tx.sign(alice.signer(), client.network_config.chain_id, alice_account.number)
    tx.sign(bob.signer(), client.network_config.chain_id, bob_account.number)

    # all done!
    tx.complete()

    print("Executing atomic swap...")
    tx = client.broadcast_tx(tx).wait_to_complete()
    print(f"Executing atomic swap...complete (tx: {tx.tx_hash})")

    # Step 4. Query what the new balance state is
    result = contract.query(
        {
            "balance_batch": {
                "addresses": [
                    {
                        "address": bob,
                        "id": TOKEN_ID_1,
                    },
                    {
                        "address": alice,
                        "id": TOKEN_ID_2,
                    },
                ]
            }
        }
    )
    print(f'Alice has {result["balances"][1]} of Bob\'s tokens')
    print(f'Bob has {result["balances"][0]} of Alice\'s tokens')


if __name__ == "__main__":
    main()
