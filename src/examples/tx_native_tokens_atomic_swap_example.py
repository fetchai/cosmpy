""" Native tokens atomic swap example """

from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from cosmos.base.v1beta1.coin_pb2 import Coin

from grpc import insecure_channel

from examples.helpers import sign_and_broadcast_msgs
from examples.helpers import get_balance, get_packed_send_msg

# Denomination and amouunt of transferred tokens
DENOM_1 = "stake"
AMOUNT_1 = [Coin(amount="1", denom=DENOM_1)]
DENOM_2 = "atestfet"
AMOUNT_2 = [Coin(amount="1", denom=DENOM_2)]

# Private key of validator's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
VALIDATOR_ADDRESS = Address(VALIDATOR_PK)

# Private key of validator's account
BOB_PK = PrivateKey(
    bytes.fromhex(
        "439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636"
    )
)
BOB_ADDRESS = Address(BOB_PK)

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Print balances before transfer
print("Before transaction")
denom_1_balance = get_balance(channel, VALIDATOR_ADDRESS, DENOM_1)
denom_2_balance = get_balance(channel, VALIDATOR_ADDRESS, DENOM_2)
print(f"Validator has {denom_1_balance.balance.amount} {DENOM_1} and {denom_2_balance.balance.amount} {DENOM_2}")
denom_1_balance = get_balance(channel, BOB_ADDRESS, DENOM_1)
denom_2_balance = get_balance(channel, BOB_ADDRESS, DENOM_2)
print(f"Bob has {denom_1_balance.balance.amount} {DENOM_1} and {denom_2_balance.balance.amount} {DENOM_2}")

# Create atomic-swap send messages
# Transfer AMOUNT_1 from validator to bob
msg_1 = get_packed_send_msg(from_address=VALIDATOR_ADDRESS,
                            to_address=BOB_ADDRESS,
                            amount=AMOUNT_1)

# Transfer AMOUNT_1 from bob to validator
msg_2 = get_packed_send_msg(from_address=BOB_ADDRESS,
                            to_address=VALIDATOR_ADDRESS,
                            amount=AMOUNT_2)

# Send and broadcast both messages as part of 1 transaction
sign_and_broadcast_msgs([msg_1, msg_2], channel, [VALIDATOR_PK, BOB_PK])

# Print balances after transfer
print("After transaction")
denom_1_balance = get_balance(channel, VALIDATOR_ADDRESS, DENOM_1)
denom_2_balance = get_balance(channel, VALIDATOR_ADDRESS, DENOM_2)
print(f"Validator has {denom_1_balance.balance.amount} {DENOM_1} and {denom_2_balance.balance.amount} {DENOM_2}")
denom_1_balance = get_balance(channel, BOB_ADDRESS, DENOM_1)
denom_2_balance = get_balance(channel, BOB_ADDRESS, DENOM_2)
print(f"Bob has {denom_1_balance.balance.amount} {DENOM_1} and {denom_2_balance.balance.amount} {DENOM_2}")
