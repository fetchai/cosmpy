""" Atomic swap using ERC1155 contract and multiple messages per transaction example """

from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from grpc import insecure_channel

from examples.helpers import sign_and_broadcast_msgs, get_packed_exec_msg, get_packed_store_msg, get_packed_init_msg, \
    query_contract_state, get_code_id, get_contract_address

# ID and amount of tokens to be minted in contract
TOKEN_ID_1 = "1234"
AMOUNT_1 = "1"
TOKEN_ID_2 = "1235"
AMOUNT_2 = "1"

# Path to smart contract
CONTRACT_FILENAME = "../../contracts/cw_erc1155.wasm"

# Private key of validator's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
VALIDATOR_ADDRESS = Address(VALIDATOR_PK)

# Private key of bob's account
BOB_PK = PrivateKey(
    bytes.fromhex(
        "439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636"
    )
)
BOB_ADDRESS = Address(BOB_PK)

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Store contract
store_msg = get_packed_store_msg(sender_address=VALIDATOR_ADDRESS,
                                 contract_filename=CONTRACT_FILENAME)
response = sign_and_broadcast_msgs(channel, [store_msg], [VALIDATOR_PK], gas_limit=2000000)
code_id = get_code_id(response)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg = get_packed_init_msg(sender_address=VALIDATOR_ADDRESS, code_id=code_id, init_msg={})
response = sign_and_broadcast_msgs(channel, [init_msg], [VALIDATOR_PK], gas_limit=2000000)
contract_address = get_contract_address(response)
print(f"Contract address: {contract_address}")

# Create token 2 tokens in one batch message
create_batch_msg = \
    {
        "create_batch":
            {
                "item_owner": str(VALIDATOR_ADDRESS),
                "tokens":
                    [
                        {
                            "id": TOKEN_ID_1,
                            "path": "some_path",
                        },
                        {
                            "id": TOKEN_ID_2,
                            "path": "some_path",
                        }
                    ]
            }
    }
exec_msg = get_packed_exec_msg(sender_address=VALIDATOR_ADDRESS,
                               contract_address=contract_address,
                               msg=create_batch_msg)
response = sign_and_broadcast_msgs(channel, [exec_msg], [VALIDATOR_PK], gas_limit=2000000)
print(f"Created tokens with ID {TOKEN_ID_1} and {TOKEN_ID_2}")

# Mint 1 token with ID TOKEN_ID_1 and give it to validator
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(VALIDATOR_ADDRESS),
                "id": TOKEN_ID_1,
                "supply": AMOUNT_1,
                "data": "some_data",
            },
    }
exec_msg = get_packed_exec_msg(sender_address=VALIDATOR_ADDRESS,
                               contract_address=contract_address,
                               msg=mint_single_msg)
response = sign_and_broadcast_msgs(channel, [exec_msg], [VALIDATOR_PK], gas_limit=2000000)
print(f"Minted 1 token with ID {TOKEN_ID_1} to validator.")

# Mint 1 token with ID TOKEN_ID_2 and give it to bob
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(BOB_ADDRESS),
                "id": TOKEN_ID_2,
                "supply": AMOUNT_2,
                "data": "some_data",
            },
    }
exec_msg = get_packed_exec_msg(sender_address=VALIDATOR_ADDRESS,
                               contract_address=contract_address,
                               msg=mint_single_msg)
response = sign_and_broadcast_msgs(channel, [exec_msg], [VALIDATOR_PK], gas_limit=2000000)
print(f"Minted 1 token with ID {TOKEN_ID_2} to bob")

# Create atomic swap messages
# Message to transfer 1 TOKEN_1 from validator to bob
transfer_msg_1 = \
    {
        "transfer_single":
            {
                "operator": str(VALIDATOR_ADDRESS),
                "from_address": str(VALIDATOR_ADDRESS),
                "to_address": str(BOB_ADDRESS),
                "id": TOKEN_ID_1,
                "value": AMOUNT_1,
            },
    }
exec_transfer_msg_1 = get_packed_exec_msg(sender_address=VALIDATOR_ADDRESS,
                                          contract_address=contract_address,
                                          msg=transfer_msg_1)

# Message to transfer 1 TOKEN_2 from bob to validator
transfer_msg_2 = \
    {
        "transfer_single":
            {
                "operator": str(BOB_ADDRESS),
                "from_address": str(BOB_ADDRESS),
                "to_address": str(VALIDATOR_ADDRESS),
                "id": TOKEN_ID_2,
                "value": AMOUNT_2,
            },
    }
exec_transfer_msg_2 = get_packed_exec_msg(sender_address=BOB_ADDRESS,
                                          contract_address=contract_address,
                                          msg=transfer_msg_2)

# Execute atomic swap by 2 transfer messages in one transaction
response = sign_and_broadcast_msgs(channel, [exec_transfer_msg_1, exec_transfer_msg_2], [VALIDATOR_PK, BOB_PK],
                                   gas_limit=2000000)
print(f"Swapped token validator's token {TOKEN_ID_1} with bob's token {TOKEN_ID_2}")

# Query validator's balances of validator an bob in one query call
msg = {
    "balance_batch":
        {
            "addresses":
                [
                    {
                        "address": str(BOB_ADDRESS),
                        "id": TOKEN_ID_1,
                    }
                    ,
                    {
                        "address": str(VALIDATOR_ADDRESS),
                        "id": TOKEN_ID_2,
                    }
                ]
        }
}
res = query_contract_state(channel=channel,
                           contract_address=contract_address,
                           msg=msg)

# Check if swap was successful
# TOKEN_ID_1 should be now owned by bob and TOKEN_ID_2 by validator
assert res["balances"] == [AMOUNT_1, AMOUNT_2]

print("All done!")
