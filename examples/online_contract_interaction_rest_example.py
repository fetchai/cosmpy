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

""" REST example of ERC1155 contract deployment and interaction on Capricorn Fetch.ai network"""

import inspect
import os
from pathlib import Path
from typing import Any, Dict

from cosmpy.clients.signing_cosmwasm_client import SigningCosmWasmClient
from cosmpy.common.rest_client import RestClient
from cosmpy.common.utils import refill_wealth_from_faucet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey

# ID and amount of tokens to be minted in contract
TOKEN_ID = "680564733841876926926749214863536422912"
AMOUNT = "1"

# Path to smart contract
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(os.path.join(CUR_PATH, "..", "contracts", "cw_erc1155.wasm"))

# Node config
REST_ENDPOINT_ADDRESS = "https://rest-capricorn.fetch.ai:443"
CHAIN_ID = "capricorn-1"
DENOM = "atestfet"

# Private key of sender's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex("0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ad")
)

# Create Rest channel
channel = RestClient(REST_ENDPOINT_ADDRESS)

# Refill balance from faucet
refill_wealth_from_faucet(
    channel,
    "https://faucet-capricorn.t-v2-london-c.fetch-ai.com",
    [Address(VALIDATOR_PK)],
    DENOM,
)

# Create signing client
validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)

# Store contract
code_id = validator_client.deploy_contract(CONTRACT_FILENAME)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg: Dict[str, Any] = {}
contract_address = validator_client.instantiate_contract(code_id, init_msg)
print(f"Contract address: {contract_address}")

# Create token with ID TOKEN_ID
create_single_msg = {
    "create_single": {
        "item_owner": str(validator_client.address),
        "id": TOKEN_ID,
        "path": "some_path",
    }
}
response = validator_client.execute_contract(contract_address, create_single_msg)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = {
    "mint_single": {
        "to_address": str(validator_client.address),
        "id": TOKEN_ID,
        "supply": AMOUNT,
        "data": "some_data",
    },
}
response = validator_client.execute_contract(contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {
    "balance": {
        "address": str(validator_client.address),
        "id": TOKEN_ID,
    }
}
res = validator_client.query_contract_state(contract_address=contract_address, msg=msg)

# Check if balance of token with ID TOKEN_ID of validator is correct
assert res["balance"] == AMOUNT
print("All done!")
