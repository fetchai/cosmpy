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

""" gRPC example of sending and querying funds """

from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import Coin, CosmosLedger

# Denomination and amount of transferred tokens
DENOM = "stake"
AMOUNT = [Coin(amount="1", denom=DENOM)]

# Node config
GRPC_ENDPOINT_ADDRESS = "localhost:9090"
CHAIN_ID = "testing"
PREFIX = "fetch"

# Private key of Validator on local net that already has funds
sender_crypto = CosmosCrypto(
    private_key_str="0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae",
    prefix=PREFIX,
)

# Address of recipient account
TO_ADDRESS = "fetch128r83uvcxns82535d3da5wmfvhc2e5mut922dw"

# Create ledger
ledger = CosmosLedger(chain_id=CHAIN_ID, rpc_node_address=GRPC_ENDPOINT_ADDRESS)

ledger.check_availability()
exit()

# Print balance before transfer
print("Before transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Validator has {res} {DENOM}")
res = ledger.get_balance(TO_ADDRESS, DENOM)
print(f"Receiver has {res} {DENOM}")

# Generate, sign and broadcast send tokens transaction
ledger.send_funds(sender_crypto, TO_ADDRESS, AMOUNT)

# Print balance after transfer
print("After transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Validator has {res} {DENOM}")
res = ledger.get_balance(TO_ADDRESS, DENOM)
print(f"Receiver has {res} {DENOM}")
