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

""" REST example of sending and querying funds using Capricorn testnet """

from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# Denomination and amount of transferred tokens
DENOM = "atestfet"
AMOUNT = [Coin(amount="1", denom=DENOM)]

# Node config
REST_ENDPOINT_ADDRESS = "https://rest-capricorn.fetch.ai:443"
FAUCET_URL = "https://faucet-capricorn.t-v2-london-c.fetch-ai.com"
CHAIN_ID = "capricorn-1"
PREFIX = "fetch"
MINIMUM_GAS_PRICE = Coin(denom=DENOM, amount=str(500000000000))

sender_crypto = CosmosCrypto(prefix=PREFIX)
receiver_crypto = CosmosCrypto(prefix=PREFIX)

# Create ledger
ledger = CosmosLedger(
    chain_id=CHAIN_ID,
    rest_node_address=REST_ENDPOINT_ADDRESS,
    minimum_gas_price=MINIMUM_GAS_PRICE,
    faucet_url=FAUCET_URL,
)

# Refill sender's balance from faucet
ledger.ensure_funds([sender_crypto.get_address()])

# Print balance before transfer
print("Before transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Sender has {res} {DENOM}")
res = ledger.get_balance(receiver_crypto.get_address(), DENOM)
print(f"Receiver has {res} {DENOM}")

# Generate, sign and broadcast send tokens transaction
ledger.send_funds(sender_crypto, receiver_crypto.get_address(), AMOUNT)

# Print balance after transfer
print("After transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Sender has {res} {DENOM}")
res = ledger.get_balance(receiver_crypto.get_address(), DENOM)
print(f"Receiver has {res} {DENOM}")
