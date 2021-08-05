""" Atomic swap using ERC1155 contract and multiple messages per transaction example """

from cosm.crypto.keypairs import PrivateKey

from cosm.clients.signing_cosmwasm_client import SigningCosmWasmClient

from cosm.query.rest_client import QueryRestClient

# ID and amount of tokens to be minted in contract
TOKEN_ID_1 = "1234"
AMOUNT_1 = "1"
TOKEN_ID_2 = "1235"
AMOUNT_2 = "1"

# Path to smart contract
CONTRACT_FILENAME = "../../contracts/cw_erc1155.wasm"

# Node config
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"

# Private key of validator's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)

# Private key of bob's account
BOB_PK = PrivateKey(
    bytes.fromhex(
        "439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636"
    )
)

# Create clients
channel = QueryRestClient(REST_ENDPOINT_ADDRESS)
validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)
bob_client = SigningCosmWasmClient(BOB_PK, channel, CHAIN_ID)

# Store contract
code_id = validator_client.store_contract(CONTRACT_FILENAME)
print(f"Contract stored, code ID: {code_id}")

# Init contract
contract_address = validator_client.instantiate(code_id, {})
print(f"Contract address: {contract_address}")

# Create token 2 tokens in one batch message
create_batch_msg = \
    {
        "create_batch":
            {
                "item_owner": str(validator_client.address),
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
response = validator_client.execute(contract_address, create_batch_msg)
print(f"Created tokens with ID {TOKEN_ID_1} and {TOKEN_ID_2}")

# Mint 1 token with ID TOKEN_ID_1 and give it to validator
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(validator_client.address),
                "id": TOKEN_ID_1,
                "supply": AMOUNT_1,
                "data": "some_data",
            },
    }
response = validator_client.execute(contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID_1} to validator.")

# Mint 1 token with ID TOKEN_ID_2 and give it to bob
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(bob_client.address),
                "id": TOKEN_ID_2,
                "supply": AMOUNT_2,
                "data": "some_data",
            },
    }
response = validator_client.execute(contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID_2} to bob")

# Create atomic swap messages
# Message to transfer 1 TOKEN_1 from validator to bob
transfer_msg_1 = \
    {
        "transfer_single":
            {
                "operator": str(validator_client.address),
                "from_address": str(validator_client.address),
                "to_address": str(bob_client.address),
                "id": TOKEN_ID_1,
                "value": AMOUNT_1,
            },
    }
exec_transfer_msg_1 = validator_client.get_packed_exec_msg(sender_address=validator_client.address,
                                                           contract_address=contract_address,
                                                           msg=transfer_msg_1)

# Message to transfer 1 TOKEN_2 from bob to validator
transfer_msg_2 = \
    {
        "transfer_single":
            {
                "operator": str(bob_client.address),
                "from_address": str(bob_client.address),
                "to_address": str(validator_client.address),
                "id": TOKEN_ID_2,
                "value": AMOUNT_2,
            },
    }
exec_transfer_msg_2 = validator_client.get_packed_exec_msg(sender_address=bob_client.address,
                                                           contract_address=contract_address,
                                                           msg=transfer_msg_2)

# Execute atomic swap by 2 transfer messages in one transaction
tx = validator_client.generate_tx([exec_transfer_msg_1, exec_transfer_msg_2],
                                  [validator_client.address, bob_client.address],
                                  [validator_client.public_key_bytes, bob_client.public_key_bytes], gas_limit=2000000)
validator_client.sign_tx(tx)
bob_client.sign_tx(tx)
response = validator_client.broadcast_tx(tx)
print(f"Swapped token validator's token {TOKEN_ID_1} with bob's token {TOKEN_ID_2}")

# Query validator's balances of validator an bob in one query call
msg = {
    "balance_batch":
        {
            "addresses":
                [
                    {
                        "address": str(bob_client.address),
                        "id": TOKEN_ID_1,
                    }
                    ,
                    {
                        "address": str(validator_client.address),
                        "id": TOKEN_ID_2,
                    }
                ]
        }
}
res = validator_client.query_contract_state(contract_address=contract_address,
                                            msg=msg)

# Check if swap was successful
# TOKEN_ID_1 should be now owned by bob and TOKEN_ID_2 by validator
assert res["balances"] == [AMOUNT_1, AMOUNT_2]

print("All done!")