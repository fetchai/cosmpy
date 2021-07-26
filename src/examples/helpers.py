from cosm.crypto.keypairs import PrivateKey
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
from cosmos.crypto.secp256k1.keys_pb2 import PubKey as ProtoPubKey
from cosmos.tx.v1beta1.service_pb2 import BroadcastTxRequest, BroadcastMode, GetTxRequest
from cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthQueryClient
from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosm.tx import sign_transaction
from cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
from cosmos.base.v1beta1.coin_pb2 import Coin

from google.protobuf.any_pb2 import Any
import time


def sign_and_broadcast_msg(send_msg_packed: Any, channel, from_pk: PrivateKey, fee=[Coin(amount="0", denom="stake")],
                           gas_limit=200000, memo="", chain_id="testing"):
    # Get address from private key
    from_address = Address(from_pk)
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

    # NOTE(pb): Commented-out code intentionally left in as example:
    # tx_body.timeout_height = 0xffffffffffffffff
    tx_body = TxBody()
    tx_body.memo = memo
    tx_body.messages.extend([send_msg_packed])

    from_pub_key_pb = ProtoPubKey()
    from_pub_key_pb.key = from_pk.public_key_bytes

    single = ModeInfo.Single()
    single.mode = SignMode.SIGN_MODE_DIRECT
    mode_info = ModeInfo(single=single)

    from_pub_key_packed = Any()
    from_pub_key_packed.Pack(from_pub_key_pb, type_url_prefix="/")
    signer_info = SignerInfo(
        public_key=from_pub_key_packed,
        mode_info=mode_info,
        sequence=account.sequence,
    )
    auth_info = AuthInfo(
        signer_infos=[signer_info],
        fee=Fee(amount=fee, gas_limit=gas_limit),
    )

    tx = Tx(body=tx_body, auth_info=auth_info)
    sign_transaction(
        tx,
        signer=from_pk,
        chain_id=chain_id,
        account_number=account.account_number,
        deterministic=True,
    )

    tx_data = tx.SerializeToString()
    broad_tx_req = BroadcastTxRequest(
        tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
    )

    broad_tx_resp = tx_client.BroadcastTx(broad_tx_req)
    tx_hash = broad_tx_resp.tx_response.txhash

    # Wait for transaction to settle
    time.sleep(5)

    tx_request = GetTxRequest(hash=tx_hash)
    tx_response = tx_client.GetTx(tx_request)

    return tx_response
