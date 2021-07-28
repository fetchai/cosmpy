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
from cosmos.tx.v1beta1.service_pb2 import BroadcastTxRequest, BroadcastMode, GetTxRequest, GetTxResponse
from cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthQueryClient
from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosm.tx import multi_sign_transaction
from cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
from cosmos.base.v1beta1.coin_pb2 import Coin

from google.protobuf.any_pb2 import Any
import time
from grpc._channel import Channel


def broadcast_tx(channel: Channel, tx: Tx, wait_time: int = 5) -> GetTxResponse:
    """
    Broadcast transaction and get receipt
    :param channel: gRPC channel
    :param tx: Transaction
    :param wait_time: Number of seconds to wait before getting transaction receipt
    :return:
    """
    tx_client = TxGrpcClient(channel)
    tx_data = tx.SerializeToString()
    broad_tx_req = BroadcastTxRequest(
        tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
    )
    broad_tx_resp = tx_client.BroadcastTx(broad_tx_req)

    if broad_tx_resp.tx_response.code != 0:
        raw_log = broad_tx_resp["raw_log"]
        raise RuntimeError(f"Transaction failed: {raw_log}")

    # Wait for transaction to settle
    time.sleep(wait_time)

    # Get transaction receipt
    tx_request = GetTxRequest(hash=broad_tx_resp.tx_response.txhash)
    tx_response = tx_client.GetTx(tx_request)

    return tx_response


def query_account_data(channel: Channel, address: Address) -> BaseAccount:
    """
    Query account data for signing
    :param channel: gRPC channel
    :param address: Address of account to query data about
    :return:
    """
    # Prepare clients
    auth_query_client = AuthQueryClient(channel)

    # Get account data for signing
    account_response = auth_query_client.Account(
        QueryAccountRequest(address=str(address))

    )
    account = BaseAccount()
    if account_response.account.Is(BaseAccount.DESCRIPTOR):
        account_response.account.Unpack(account)
    else:
        raise TypeError("Unexpected account type")
    return account


def get_signer_info(from_pk: PrivateKey, from_acc: BaseAccount) -> SignerInfo:
    """
    Generate signer info
    :param from_pk: Private key of signer
    :param from_acc: Account info of signer
    :return: SignerInfo
    """
    from_pub_key_packed = Any()
    from_pub_key_pb = ProtoPubKey(key=from_pk.public_key_bytes)
    from_pub_key_packed.Pack(from_pub_key_pb, type_url_prefix="/")

    # Prepare auth info
    single = ModeInfo.Single(mode=SignMode.SIGN_MODE_DIRECT)
    mode_info = ModeInfo(single=single)
    signer_info = SignerInfo(
        public_key=from_pub_key_packed,
        mode_info=mode_info,
        sequence=from_acc.sequence,
    )
    return signer_info


def sign_and_broadcast_msgs(packed_msgs: [Any], channel: Channel, signers_keys: [PrivateKey],
                            fee: [Coin] = [Coin(amount="0", denom="stake")],
                            gas_limit: int = 200000, memo: str = "", chain_id: str = "testing",
                            wait_time: int = 5) -> GetTxResponse:
    """
    Sign and broadcast one or multiple packed Any messages

    :param packed_msgs: Messages to be broadcast
    :param channel: gRPC channel
    :param signers_keys: Private keys to sign messages
    :param fee: Transaction fee
    :param gas_limit: Gas limit
    :param memo: Memo
    :param chain_id: Chain ID
    :param wait_time: Number of seconds to wait before getting transaction receipt

    :return: Transaction receipt
    """

    # Get signers and account info
    accounts = []
    signers_info = []
    for signer_key in signers_keys:
        account = query_account_data(channel, Address(signer_key))
        accounts.append(account)
        signers_info.append(get_signer_info(signer_key, account))

    # Prepare auth info
    auth_info = AuthInfo(
        signer_infos=signers_info,
        fee=Fee(amount=fee, gas_limit=gas_limit),
    )

    # Prepare Tx body
    tx_body = TxBody()
    tx_body.memo = memo
    tx_body.messages.extend(packed_msgs)

    # Prepare and sign transaction
    tx = Tx(body=tx_body, auth_info=auth_info)
    multi_sign_transaction(
        tx,
        signers=signers_keys,
        chain_id=chain_id,
        accounts=accounts,
        deterministic=True,
    )

    return broadcast_tx(channel, tx, wait_time)
