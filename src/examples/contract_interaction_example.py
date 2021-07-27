import gzip
import json
from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from cosmwasm.wasm.v1beta1.tx_pb2 import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from cosmwasm.wasm.v1beta1.query_pb2_grpc import QueryStub as CosmWasmQueryClient
from cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest

from cosmos.base.v1beta1.coin_pb2 import Coin
from pathlib import Path
from grpc import insecure_channel
from common import JSONLike

from google.protobuf.any_pb2 import Any

from examples.helpers import sign_and_broadcast_msg


def get_code_id(response: str) -> int:
    """
    Get code id from store code transaction response
    :param response: Response of store code transaction
    :return: integer code_id
    """
    raw_log = json.loads(response.tx_response.raw_log)
    assert raw_log[0]["events"][0]["attributes"][3]["key"] == "code_id"
    return int(raw_log[0]["events"][0]["attributes"][3]["value"])


def get_packed_store_msg(sender_address: Address, contract_filename: Path) -> Any:
    """
    Loads contract bytecode, generate and return packed MsgStoreCode
    :param sender_address: Address of transaction sender
    :param contract_filename: Path to smart contract bytecode
    :return: Packed MsgStoreCode
    """
    with open(contract_filename, "rb") as contract_file:
        wasm_byte_code = gzip.compress(contract_file.read(), 6)

    msg_send = MsgStoreCode(sender=str(sender_address),
                            wasm_byte_code=wasm_byte_code,
                            )
    send_msg_packed = Any()
    send_msg_packed.Pack(msg_send, type_url_prefix="/")

    return send_msg_packed


def get_contract_address(response: str) -> str:
    """
    Get contract address from instantiate msg response
    :param response: Response of MsgInstantiateContract transaction
    :return: contract address string
    """
    raw_log = json.loads(response.tx_response.raw_log)
    assert raw_log[0]["events"][1]["attributes"][0]["key"] == "contract_address"
    return str(raw_log[0]["events"][1]["attributes"][0]["value"])


def get_packed_init_msg(sender_address: Address, code_id: int, init_msg: JSONLike, label="contract",
                        funds: [Coin] = []) -> Any:
    """
    Create and pack MsgInstantiateContract
    :param sender_address: Sender's address
    :param code_id: code_id of stored contract bytecode
    :param init_msg: Parameters to be passed to smart contract constructor
    :param label: Label
    :param funds: Funds transfered to new contract
    :return: Packed MsgInstantiateContract
    """
    msg_send = MsgInstantiateContract(sender=str(sender_address),
                                      code_id=code_id,
                                      init_msg=json.dumps(init_msg).encode("UTF8"),
                                      label=label,
                                      funds=funds
                                      )
    send_msg_packed = Any()
    send_msg_packed.Pack(msg_send, type_url_prefix="/")

    return send_msg_packed


def get_packed_exec_msg(sender_address: Address, contract_address: str, msg: JSONLike, funds: [Coin] = []) -> Any:
    """
    Create and pack MsgExecuteContract
    :param sender_address: Address of sender
    :param contract_address: Address of contract
    :param msg: Paramaters to be passed to smart contract
    :param funds: Funds to be sent to smart contract
    :return: Packed MsgExecuteContract
    """
    msg_send = MsgExecuteContract(sender=str(sender_address),
                                  contract=contract_address,
                                  msg=json.dumps(msg).encode("UTF8"),
                                  funds=funds
                                  )
    send_msg_packed = Any()
    send_msg_packed.Pack(msg_send, type_url_prefix="/")

    return send_msg_packed


def query_contract_state(contract_address: str, msg: JSONLike) -> JSONLike:
    """
    Get state of smart contract
    :param contract_address: Contract address
    :param msg: Parameters to be passed to query function inside contract
    :return: JSON query response
    """
    request = QuerySmartContractStateRequest(address=contract_address,
                                             query_data=json.dumps(msg).encode("UTF8"))
    res = wasm_query_client.SmartContractState(request)
    return json.loads(res.data)


"""
    Smart contract interaction example
"""

# Private key of sender's account
from_pk = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Prepare client for querying contract state
wasm_query_client = CosmWasmQueryClient(channel)

# Store contract
store_msg = get_packed_store_msg(sender_address=Address(from_pk),
                                 contract_filename="../../contracts/cw_erc1155.wasm")
response = sign_and_broadcast_msg(store_msg, channel, from_pk, gas_limit=2000000)
code_id = get_code_id(response)
print(f"Contract stored, code ID: {code_id}")

# Init contract
init_msg = get_packed_init_msg(sender_address=Address(from_pk), code_id=code_id, init_msg={})
response = sign_and_broadcast_msg(init_msg, channel, from_pk, gas_limit=2000000)
contract_address = get_contract_address(response)
print(f"Contract address: {contract_address}")

# Create token with ID 1234
create_single_msg = \
    {
        "create_single":
            {
                "item_owner": str(Address(from_pk)),
                "id": "1234",
                "path": "some_path",
            }
    }
exec_msg = get_packed_exec_msg(sender_address=Address(from_pk),
                               contract_address=contract_address,
                               msg=create_single_msg)
response = sign_and_broadcast_msg(exec_msg, channel, from_pk, gas_limit=2000000)
print("Created token with ID 1234")

# Mint 1 token with ID 1234 and give it to validator
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(Address(from_pk)),
                "id": "1234",
                "supply": "1",
                "data": "some_data",
            },
    }
exec_msg = get_packed_exec_msg(sender_address=Address(from_pk),
                               contract_address=contract_address,
                               msg=mint_single_msg)
response = sign_and_broadcast_msg(exec_msg, channel, from_pk, gas_limit=2000000)
print("Minted 1 token with ID 1234")

# Query validator's balance of token 1234
msg = {"balance": {
    "address": str(Address(from_pk)),
    "id": "1234",
}}
res = query_contract_state(contract_address=contract_address,
                           msg=msg)
# Check if balance is 1
assert res["balance"] == "1"
print("All done!")
