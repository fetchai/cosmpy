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

""" REST example of sending and querying funds """

from cosmpy.clients.signing_cosmwasm_client import SigningCosmWasmClient
from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# Denomination and amount of transferred tokens
DENOM = "stake"
AMOUNT = [Coin(amount="1", denom=DENOM)]

# Node config
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"

# Private key of sender's account
FROM_PK = PrivateKey(
    bytes.fromhex("0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae")
)
# Create client
channel = RestClient(REST_ENDPOINT_ADDRESS)
client = SigningCosmWasmClient(FROM_PK, channel, CHAIN_ID)

# Address of recipient account
TO_ADDRESS = Address("fetch128r83uvcxns82535d3da5wmfvhc2e5mut922dw")

# Print balance before transfer
print("Before transaction")
res = client.get_balance(client.address, DENOM)
print(f"Validator has {res.balance.amount} {DENOM}")
res = client.get_balance(TO_ADDRESS, DENOM)
print(f"Bob has {res.balance.amount} {DENOM}")

# Generate, sign and broadcast send tokens transaction
client.send_tokens(TO_ADDRESS, AMOUNT)

# Print balance after transfer
print("After transaction")
res = client.get_balance(client.address, DENOM)
print(f"Validator has {res.balance.amount} {DENOM}")
res = client.get_balance(TO_ADDRESS, DENOM)
print(f"Bob has {res.balance.amount} {DENOM}")
