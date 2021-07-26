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
from grpc._channel import Channel


def sign_and_broadcast_msg(send_msg_packed: Any, channel: Channel, from_pk: PrivateKey,
                           fee: [Coin] = [Coin(amount="0", denom="stake")],
                           gas_limit: int = 200000, memo: str = "", chain_id: str = "testing"):
    """
    Sign and broadcast packed Any message
    :param send_msg_packed: Message to be broadcast
    :param channel: gRPC channel
    :param from_pk: Sender's private key
    :param fee: Transaction fee
    :param gas_limit: Gas limit
    :param memo: Memo
    :param chain_id: Chain ID
    :return: Transaction receipt
    """
    # Prepare clients
    auth_query_client = AuthQueryClient(channel)
    tx_client = TxGrpcClient(channel)

    # Get address from private key
    from_address = Address(from_pk)

    # Get account data for signing
    account_response = auth_query_client.Account(
        QueryAccountRequest(address=str(from_address))
    )
    account = BaseAccount()
    if account_response.account.Is(BaseAccount.DESCRIPTOR):
        account_response.account.Unpack(account)
    else:
        raise TypeError("Unexpected account type")

    # Prepare Tx body
    tx_body = TxBody()
    tx_body.memo = memo
    tx_body.messages.extend([send_msg_packed])

    from_pub_key_packed = Any()
    from_pub_key_pb = ProtoPubKey(key=from_pk.public_key_bytes)
    from_pub_key_packed.Pack(from_pub_key_pb, type_url_prefix="/")

    # Prepare auth info
    single = ModeInfo.Single(mode=SignMode.SIGN_MODE_DIRECT)
    mode_info = ModeInfo(single=single)
    signer_info = SignerInfo(
        public_key=from_pub_key_packed,
        mode_info=mode_info,
        sequence=account.sequence,
    )
    auth_info = AuthInfo(
        signer_infos=[signer_info],
        fee=Fee(amount=fee, gas_limit=gas_limit),
    )

    # Prepare and sign transaction
    tx = Tx(body=tx_body, auth_info=auth_info)
    sign_transaction(
        tx,
        signer=from_pk,
        chain_id=chain_id,
        account_number=account.account_number,
        deterministic=True,
    )

    # Broadcast transaction
    tx_data = tx.SerializeToString()
    broad_tx_req = BroadcastTxRequest(
        tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
    )
    broad_tx_resp = tx_client.BroadcastTx(broad_tx_req)

    # Wait for transaction to settle
    time.sleep(5)

    # Get transaction receipt
    tx_request = GetTxRequest(hash=broad_tx_resp.tx_response.txhash)
    tx_response = tx_client.GetTx(tx_request)

    return tx_response
