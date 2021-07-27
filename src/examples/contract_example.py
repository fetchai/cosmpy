import gzip
import json
from cosm.crypto.keypairs import PrivateKey
from cosm.crypto.address import Address
from cosmwasm.wasm.v1beta1.tx_pb2 import MsgStoreCode
from cosmos.base.v1beta1.coin_pb2 import Coin
from pathlib import Path
from grpc import insecure_channel

from google.protobuf.any_pb2 import Any

from examples.helpers import sign_and_broadcast_msg


def get_code_id(response: str):
    raw_log = json.loads(response.tx_response.raw_log)
    return int(raw_log[0]["events"][0]["attributes"][3]["value"])


def get_packed_store_msg(deployer_address: Address, contract_filename: Path, source: str = "", builder: str = ""):
    with open(contract_filename, "rb") as contract_file:
        wasm_byte_code = gzip.compress(contract_file.read(), 6)

    msg_send = MsgStoreCode(sender=str(deployer_address),
                            wasm_byte_code=wasm_byte_code,
                            source=source,
                            builder=builder
                            )
    send_msg_packed = Any()
    send_msg_packed.Pack(msg_send, type_url_prefix="/")

    return send_msg_packed


# Private key of sender's account
from_pk = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)

# Open gRPC channel
channel = insecure_channel("localhost:9090")

# Store contract
store_msg = get_packed_store_msg(deployer_address=Address(from_pk),
                                 contract_filename="../../contracts/cw_erc1155.wasm")
response = sign_and_broadcast_msg(store_msg, channel, from_pk, gas_limit=2000000)
code_id = get_code_id(response)
print("Contract stored, code ID: ", code_id)
