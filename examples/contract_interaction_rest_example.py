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

""" REST example of ERC1155 contract deployment and interaction """

import inspect
import os
from pathlib import Path
from typing import Any, Dict

from cosmpy.clients.signing_cosmwasm_client import SigningCosmWasmClient
from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.keypairs import PrivateKey

# ID and amount of tokens to be minted in contract
TOKEN_ID = "1234"
AMOUNT = "1"

# Path to smart contract
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(os.path.join(CUR_PATH, "..", "contracts", "cw_erc1155.wasm"))

# Node config
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"

# Private key of sender's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex("0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae")
)

# Create client
channel = RestClient(REST_ENDPOINT_ADDRESS)
client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)

# Store contract
code_id = client.deploy_contract(CONTRACT_FILENAME)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg: Dict[str, Any] = {}
contract_address = client.instantiate_contract(code_id, init_msg)
print(f"Contract address: {contract_address}")

# Create token with ID TOKEN_ID
create_single_msg = {
    "create_single": {
        "item_owner": str(client.address),
        "id": TOKEN_ID,
        "path": "some_path",
    }
}
response = client.execute_contract(contract_address, create_single_msg)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = {
    "mint_single": {
        "to_address": str(client.address),
        "id": TOKEN_ID,
        "supply": AMOUNT,
        "data": "some_data",
    },
}
response = client.execute_contract(contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {
    "balance": {
        "address": str(client.address),
        "id": TOKEN_ID,
    }
}
res = client.query_contract_state(contract_address=contract_address, msg=msg)

# Check if balance of token with ID TOKEN_ID of validator is correct
assert res["balance"] == AMOUNT
print("All done!")
