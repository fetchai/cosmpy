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

""" REST example of ERC1155 contract deployment and interaction using CosmosLedger"""
import inspect
import os
from pathlib import Path
from typing import Any, Dict

from cosmpy.ledger.ledger import CosmosLedger

# ID and amount of tokens to be minted in contract
TOKEN_ID = "680564733841876926926749214863536422912"
AMOUNT = "1"

# Path to smart contract
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(os.path.join(CUR_PATH, "..", "contracts", "cw_erc1155.wasm"))

# Node config
REST_ENDPOINT_ADDRESS = "https://rest-capricorn.fetch.ai:443"
FAUCET_ADDRESS = "https://faucet-capricorn.t-v2-london-c.fetch-ai.com"
CHAIN_ID = "capricorn-1"
DENOM = "atestfet"
PREFIX = "fetch"

ledger = CosmosLedger(
    node_address=REST_ENDPOINT_ADDRESS,
    denom=DENOM,
    chain_id=CHAIN_ID,
    prefix=PREFIX,
    faucet_url=FAUCET_ADDRESS,
)

user_crypto = ledger.make_new_crypto()
print(f"User address: {user_crypto.get_address()}")
print(f"User balance: {ledger.get_balance(user_crypto.get_address())}")

# Refill balance from faucet
print("Refilling funds from faucet.")
ledger.ensure_funds([user_crypto.get_address()])
print(f"User balance: {ledger.get_balance(user_crypto.get_address())}")

code_id, _ = ledger.deploy_contract(user_crypto, CONTRACT_FILENAME)
print(f"Code ID: {code_id}")

init_msg: Dict[str, Any] = {}
contract_address, _ = ledger.send_init_msg(user_crypto, code_id, init_msg, "some_label")
print(f"Contract address: {contract_address}")


# Create token with ID TOKEN_ID
create_single_msg = {
    "create_single": {
        "item_owner": user_crypto.get_address(),
        "id": TOKEN_ID,
        "path": "some_path",
    }
}
ledger.send_execute_msg(user_crypto, contract_address, create_single_msg)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = {
    "mint_single": {
        "to_address": user_crypto.get_address(),
        "id": TOKEN_ID,
        "supply": AMOUNT,
        "data": "some_data",
    },
}
response = ledger.send_execute_msg(user_crypto, contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {
    "balance": {
        "address": user_crypto.get_address(),
        "id": TOKEN_ID,
    }
}
res = ledger.send_query_msg(contract_address, msg)

# Check if balance of token with ID TOKEN_ID of validator is correct
assert res["balance"] == AMOUNT
print("All done!")
