import os
from cosm.crypto.keypairs import PublicKey, PrivateKey
from cosm.crypto.address import Address
from cosmos.tx.v1beta1.tx_pb2 import (
    Tx,
    TxBody,
    SignerInfo,
    AuthInfo,
    ModeInfo,
    Fee,
)
from cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmos.base.v1beta1.coin_pb2 import Coin
from cosmos.crypto.secp256k1.keys_pb2 import PubKey as ProtoPubKey
from grpc import insecure_channel

from cosmos.tx.v1beta1.service_pb2 import BroadcastTxRequest, BroadcastMode
from cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthQueryClient
from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from google.protobuf.any_pb2 import Any
from cosm.tx import sign_transaction
from cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient


from_pk = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
from_address = Address(from_pk)
print("validator = ", from_address)

to_pb = PrivateKey(
    bytes.fromhex(
        "439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636"
    )
)
to_address = Address(to_pb)
print("bob = ", to_address)

channel = insecure_channel("localhost:9090")
tx_client = TxGrpcClient(channel)

auth_query_client = AuthQueryClient(channel)
account_response = auth_query_client.Account(
    QueryAccountRequest(address=str(from_address))
)
account = BaseAccount()
if account_response.account.Is(BaseAccount.DESCRIPTOR):
    account_response.account.Unpack(account)
else:
    raise TypeError("Unexpected account type")
print("account = ", account)

msg_send = MsgSend()
msg_send.from_address = str(from_address)
msg_send.to_address = str(to_address)
amount = Coin()
amount.amount = "1234"
amount.denom = "stake"
msg_send.amount.extend([amount])

tx_body = TxBody()
tx_body.memo = "very first tx"
# NOTE(pb): Commented-out code intentionally left in as example:
# tx_body.timeout_height = 0xffffffffffffffff
send_msg_packed = Any()
send_msg_packed.Pack(msg_send)  # , type_url_prefix="/")
tx_body.messages.extend([send_msg_packed])

from_pub_key_pb = ProtoPubKey()
from_pub_key_pb.key = from_pk.public_key_bytes

single = ModeInfo.Single()
single.mode = SignMode.SIGN_MODE_DIRECT
mode_info = ModeInfo(single=single)

from_pub_key_packed = Any()
from_pub_key_packed.Pack(from_pub_key_pb)  # , type_url_prefix="/")
signer_info = SignerInfo(
    public_key=from_pub_key_packed,
    mode_info=mode_info,
    sequence=account.sequence,
)
auth_info = AuthInfo(
    signer_infos=[signer_info],
    fee=Fee(amount=[Coin(amount="0", denom="stake")], gas_limit=200000),
)

tx = Tx(body=tx_body, auth_info=auth_info)
sign_transaction(
    tx,
    signer=from_pk,
    chain_id="testing",
    account_number=account.account_number,
    deterministic=True,
)
print("new Tx = ", tx)

tx_data = tx.SerializeToString()
broad_tx_req = BroadcastTxRequest(
    tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
)

broad_tx_resp = tx_client.BroadcastTx(broad_tx_req)

print("broad_tx_resp = ", broad_tx_resp)
