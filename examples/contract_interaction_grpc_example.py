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

""" gRPC example of ERC1155 contract deployment and interaction """

import inspect
import os
from pathlib import Path
from typing import Any, Dict

from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger

# ID and amount of tokens to be minted in contract
TOKEN_ID = "680564733841876926926749214863536422912"
AMOUNT = "1"

# Path to smart contract
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(os.path.join(CUR_PATH, "..", "contracts", "cw_erc1155.wasm"))

# Node config
GRPC_ENDPOINT_ADDRESS = "localhost:9090"
CHAIN_ID = "testing"
DENOM = "atestfet"
PREFIX = "fetch"

ledger = CosmosLedger(
    rpc_node_address=GRPC_ENDPOINT_ADDRESS,
    chain_id=CHAIN_ID,
)

# Private key of Validator on local net that already has funds
validator_crypto = CosmosCrypto(
    private_key_str="0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae",
    prefix=PREFIX,
)

code_id, _ = ledger.deploy_contract(validator_crypto, CONTRACT_FILENAME)
print(f"Code ID: {code_id}")

init_msg: Dict[str, Any] = {}
contract_address, _ = ledger.send_init_msg(
    validator_crypto, code_id, init_msg, "some_label"
)
print(f"Contract address: {contract_address}")


# Create token with ID TOKEN_ID
create_single_msg = {
    "create_single": {
        "item_owner": validator_crypto.get_address(),
        "id": TOKEN_ID,
        "path": "some_path",
    }
}
ledger.send_execute_msg(validator_crypto, contract_address, create_single_msg)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = {
    "mint_single": {
        "to_address": validator_crypto.get_address(),
        "id": TOKEN_ID,
        "supply": AMOUNT,
        "data": "some_data",
    },
}
response = ledger.send_execute_msg(validator_crypto, contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {
    "balance": {
        "address": validator_crypto.get_address(),
        "id": TOKEN_ID,
    }
}
res = ledger.query_contract_state(contract_address, msg)

# Check if balance of token with ID TOKEN_ID of validator is correct
assert res["balance"] == AMOUNT
print("All done!")
