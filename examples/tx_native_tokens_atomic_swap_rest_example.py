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

""" REST example of native tokens atomic swap """

from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# Denomination and amount of transferred tokens
DENOM_1 = "stake"
AMOUNT_1 = [Coin(amount="1", denom=DENOM_1)]
DENOM_2 = "atestfet"
AMOUNT_2 = [Coin(amount="1", denom=DENOM_2)]

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

# Print balances before transfer
print("Before transaction")
denom_1_balance = ledger.get_balance(validator_crypto.get_address(), DENOM_1)
denom_2_balance = ledger.get_balance(validator_crypto.get_address(), DENOM_2)
print(f"Validator has {denom_1_balance} {DENOM_1} and {denom_2_balance} {DENOM_2}")
denom_1_balance = ledger.get_balance(bob_crypto.get_address(), DENOM_1)
denom_2_balance = ledger.get_balance(bob_crypto.get_address(), DENOM_2)
print(f"Bob has {denom_1_balance} {DENOM_1} and {denom_2_balance} {DENOM_2}")

# Create atomic-swap send messages
# Transfer AMOUNT_1 from validator to bob
msg_1 = ledger.get_packed_send_msg(
    from_address=validator_crypto.get_address(),
    to_address=bob_crypto.get_address(),
    amount=AMOUNT_1,
)

# Transfer AMOUNT_2 from bob to validator
msg_2 = ledger.get_packed_send_msg(
    from_address=bob_crypto.get_address(),
    to_address=validator_crypto.get_address(),
    amount=AMOUNT_2,
)

# Generate one transaction containing both messages
tx = ledger.generate_tx(
    packed_msgs=[msg_1, msg_2],
    from_addresses=[validator_crypto.get_address(), bob_crypto.get_address()],
    pub_keys=[validator_crypto.get_pubkey_as_bytes(), bob_crypto.get_pubkey_as_bytes()],
)

# Sign transaction by both clients
ledger.sign_tx(validator_crypto, tx)
ledger.sign_tx(bob_crypto, tx)

# Broadcast transaction
ledger.broadcast_tx(tx)

# Print balances after transfer
print("After transaction")
denom_1_balance = ledger.get_balance(validator_crypto.get_address(), DENOM_1)
denom_2_balance = ledger.get_balance(validator_crypto.get_address(), DENOM_2)
print(f"Validator has {denom_1_balance} {DENOM_1} and {denom_2_balance} {DENOM_2}")
denom_1_balance = ledger.get_balance(bob_crypto.get_address(), DENOM_1)
denom_2_balance = ledger.get_balance(bob_crypto.get_address(), DENOM_2)
print(f"Bob has {denom_1_balance} {DENOM_1} and {denom_2_balance} {DENOM_2}")
