""" Smart contract interaction example """

from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from grpc import insecure_channel

from examples.helpers import sign_and_broadcast_msgs, get_packed_exec_msg, get_packed_store_msg, get_packed_init_msg, query_contract_state, get_code_id, get_contract_address

# ID and amount of tokens to be minted in contract
TOKEN_ID = "1234"
AMOUNT = "1"

# Path to smart contract
CONTRACT_FILENAME = "../../contracts/cw_erc1155.wasm"

# Private key of sender's account
FROM_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
FROM_ADDRESS = Address(FROM_PK)

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Prepare client for querying contract state

# Store contract
store_msg = get_packed_store_msg(sender_address=FROM_ADDRESS,
                                 contract_filename=CONTRACT_FILENAME)
response = sign_and_broadcast_msgs([store_msg], channel, [FROM_PK], gas_limit=2000000)
code_id = get_code_id(response)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg = get_packed_init_msg(sender_address=FROM_ADDRESS, code_id=code_id, init_msg={})
response = sign_and_broadcast_msgs([init_msg], channel, [FROM_PK], gas_limit=2000000)
contract_address = get_contract_address(response)
print(f"Contract address: {contract_address}")

# Create token with ID TOKEN_ID
create_single_msg = \
    {
        "create_single":
            {
                "item_owner": str(FROM_ADDRESS),
                "id": TOKEN_ID,
                "path": "some_path",
            }
    }
exec_msg = get_packed_exec_msg(sender_address=FROM_ADDRESS,
                               contract_address=contract_address,
                               msg=create_single_msg)
response = sign_and_broadcast_msgs([exec_msg], channel, [FROM_PK], gas_limit=2000000)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(FROM_ADDRESS),
                "id": TOKEN_ID,
                "supply": "1",
                "data": "some_data",
            },
    }
exec_msg = get_packed_exec_msg(sender_address=FROM_ADDRESS,
                               contract_address=contract_address,
                               msg=mint_single_msg)
response = sign_and_broadcast_msgs([exec_msg], channel, [FROM_PK], gas_limit=2000000)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {"balance": {
    "address": str(FROM_ADDRESS),
    "id": TOKEN_ID,
}}
res = query_contract_state(channel=channel,
                           contract_address=contract_address,
                           msg=msg)
# Check if balance is 1
assert res["balance"] == "1"
print("All done!")
