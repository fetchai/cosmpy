""" Sending and querying funds example """

from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from cosmos.base.v1beta1.coin_pb2 import Coin

from grpc import insecure_channel

from examples.helpers import sign_and_broadcast_msgs
from examples.helpers import get_balance, get_packed_send_msg

# Denomination and amouunt of transferred tokens
DENOM = "stake"
AMOUNT = [Coin(amount="1", denom=DENOM)]

# Private key of sender's account
FROM_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
FROM_ADDRESS = Address(FROM_PK)

# Address of recipient account
TO_ADDRESS = "fetch128r83uvcxns82535d3da5wmfvhc2e5mut922dw"

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Print balance before transfer
print("Before transaction")
res = get_balance(channel, FROM_ADDRESS, DENOM)
print(f"Validator has {res.balance.amount} {DENOM}")
res = get_balance(channel, TO_ADDRESS, DENOM)
print(f"Bob has {res.balance.amount} {DENOM}")

# Create send message
msg = get_packed_send_msg(from_address=FROM_ADDRESS,
                          to_address=TO_ADDRESS,
                          amount=AMOUNT)

# Send and broadcast message
sign_and_broadcast_msgs(channel, [msg], [FROM_PK])

# Print balance after transfer
print("After transaction")
res = get_balance(channel, FROM_ADDRESS, DENOM)
print(f"Validator has {res.balance.amount} {DENOM}")
res = get_balance(channel, TO_ADDRESS, DENOM)
print(f"Bob has {res.balance.amount} {DENOM}")
