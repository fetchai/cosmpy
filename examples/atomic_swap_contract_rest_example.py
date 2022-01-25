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

""" REST example of atomic swap using ERC1155 contract and multiple messages per transaction """

import inspect
import os
from pathlib import Path
from typing import Any, Dict

from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger

# ID and amount of tokens to be minted in contract
TOKEN_ID_1 = "680564733841876926926749214863536422912"
AMOUNT_1 = "1"
TOKEN_ID_2 = "680564733841876926926749214863536422913"
AMOUNT_2 = "1"

# Path to smart contract
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(os.path.join(CUR_PATH, "..", "contracts", "cw_erc1155.wasm"))

# Node config
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"
PREFIX = "fetch"

# Private key of Validator on local net that already has funds
validator_crypto = CosmosCrypto(
    private_key_str="0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae",
    prefix=PREFIX,
)

# Private key of bob's account
bob_crypto = CosmosCrypto(
    private_key_str="439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636",
    prefix=PREFIX,
)

ledger = CosmosLedger(
    rest_node_address=REST_ENDPOINT_ADDRESS,
    chain_id=CHAIN_ID,
)

# Store contract
code_id, _ = ledger.deploy_contract(validator_crypto, CONTRACT_FILENAME)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg: Dict[str, Any] = {}
contract_address, _ = ledger.send_init_msg(
    validator_crypto, code_id, init_msg, "some_label"
)
print(f"Contract address: {contract_address}")

# Create 2 tokens in one batch message
create_batch_msg = {
    "create_batch": {
        "item_owner": str(validator_crypto.get_address()),
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
ledger.send_execute_msg(validator_crypto, contract_address, create_batch_msg)
print(f"Created tokens with ID {TOKEN_ID_1} and {TOKEN_ID_2}")

# Mint 1 token with ID TOKEN_ID_1 and give it to validator
mint_single_msg = {
    "mint_single": {
        "to_address": str(validator_crypto.get_address()),
        "id": TOKEN_ID_1,
        "supply": AMOUNT_1,
        "data": "some_data",
    },
}
response = ledger.send_execute_msg(validator_crypto, contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID_1} to validator.")

# Mint 1 token with ID TOKEN_ID_2 and give it to bob
mint_single_msg = {
    "mint_single": {
        "to_address": str(bob_crypto.get_address()),
        "id": TOKEN_ID_2,
        "supply": AMOUNT_2,
        "data": "some_data",
    },
}
response = ledger.send_execute_msg(validator_crypto, contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID_2} to bob")

# Create atomic swap messages
# Message to transfer 1 TOKEN_1 from validator to bob
transfer_msg_1 = {
    "transfer_single": {
        "operator": str(validator_crypto.get_address()),
        "from_address": str(validator_crypto.get_address()),
        "to_address": str(bob_crypto.get_address()),
        "id": TOKEN_ID_1,
        "value": AMOUNT_1,
    },
}
exec_transfer_msg_1 = ledger.get_packed_exec_msg(
    sender_address=validator_crypto.get_address(),
    contract_address=contract_address,
    msg=transfer_msg_1,
)

# Message to transfer 1 TOKEN_2 from bob to validator
transfer_msg_2 = {
    "transfer_single": {
        "operator": str(bob_crypto.get_address()),
        "from_address": str(bob_crypto.get_address()),
        "to_address": str(validator_crypto.get_address()),
        "id": TOKEN_ID_2,
        "value": AMOUNT_2,
    },
}
exec_transfer_msg_2 = ledger.get_packed_exec_msg(
    sender_address=bob_crypto.get_address(),
    contract_address=contract_address,
    msg=transfer_msg_2,
)

# Execute atomic swap by 2 transfer messages in one transaction
tx = ledger.generate_tx(
    [exec_transfer_msg_1, exec_transfer_msg_2],
    [validator_crypto.get_address(), bob_crypto.get_address()],
    [validator_crypto.get_pubkey_as_bytes(), bob_crypto.get_pubkey_as_bytes()],
    gas_limit=2000000,
)
ledger.sign_tx(validator_crypto, tx)
ledger.sign_tx(bob_crypto, tx)
response = ledger.broadcast_tx(tx)
print(f"Swapped token validator's token {TOKEN_ID_1} with bob's token {TOKEN_ID_2}")

# Query validator's balances of validator an bob in one query call
msg = {
    "balance_batch": {
        "addresses": [
            {
                "address": str(bob_crypto.get_address()),
                "id": TOKEN_ID_1,
            },
            {
                "address": str(validator_crypto.get_address()),
                "id": TOKEN_ID_2,
            },
        ]
    }
}
res = ledger.query_contract_state(contract_address=contract_address, msg=msg)

# Check if swap was successful
# TOKEN_ID_1 should be now owned by bob and TOKEN_ID_2 by validator
assert res["balances"] == [AMOUNT_1, AMOUNT_2]

print("All done!")
