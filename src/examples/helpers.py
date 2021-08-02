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
from cosm.tx import sign_transaction
from cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
from cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankQueryClent
from cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest, QueryBalanceResponse
from cosmwasm.wasm.v1beta1.query_pb2_grpc import QueryStub as CosmWasmQueryClient

import time
from grpc._channel import Channel

import gzip
import json

from cosmwasm.wasm.v1beta1.tx_pb2 import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest

from cosmos.base.v1beta1.coin_pb2 import Coin
from pathlib import Path
from common import JSONLike

from google.protobuf.any_pb2 import Any

from typing import List


def get_balance(channel: Channel, address: Address, denom: str) -> QueryBalanceResponse:
    """
    Get balance of specific account and denom

    :param channel: gRPC channel
    :param address: Address
    :param denom: Denomination

    :return: QueryBalanceResponse
    """
    bank_client = BankQueryClent(channel)
    res = bank_client.Balance(QueryBalanceRequest(address=str(address), denom=denom))
    return res


def get_packed_send_msg(from_address: Address, to_address: Address, amount: List[Coin]):
    """
    Generate and pack MsgSend

    :param from_address: Address of sender
    :param to_address: Address of recipient
    :param amount: List of Coins to be sent

    :return: packer Any type message
    """
    msg_send = MsgSend(from_address=str(from_address),
                       to_address=str(to_address),
                       amount=amount)
    send_msg_packed = Any()
    send_msg_packed.Pack(msg_send, type_url_prefix="/")

    return send_msg_packed


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
        raw_log = broad_tx_resp.tx_response.raw_log
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


def get_signer_info(from_acc: BaseAccount) -> SignerInfo:
    """
    Generate signer info
    :param from_acc: Account info of signer
    :return: SignerInfo
    """

    from_pub_key_packed = Any()
    from_pub_key_pb = ProtoPubKey(key=from_acc.pub_key.value[2:35])
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


def generate_tx(packed_msgs: List[Any], accounts: List[BaseAccount]):



# CosmWasm helpers
def sign_and_broadcast_msgs(packed_msgs: List[Any], channel: Channel, signers_keys: List[PrivateKey],
                            fee: List[Coin] = [Coin(amount="0", denom="stake")],
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
    accounts: List[BaseAccount] = []
    signers_info: List[SignerInfo] = []
    for signer_key in signers_keys:
        account = query_account_data(channel, Address(signer_key))
        accounts.append(account)
        signers_info.append(get_signer_info(account))

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

    for i in range(len(signers_keys)):
        sign_transaction(tx, signers_keys[i], chain_id, accounts[i].account_number)

    return broadcast_tx(channel, tx, wait_time)


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
                        funds: List[Coin] = []) -> Any:
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


def get_packed_exec_msg(sender_address: Address, contract_address: str, msg: JSONLike, funds: List[Coin] = []) -> Any:
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


def query_contract_state(channel: Channel, contract_address: str, msg: JSONLike) -> JSONLike:
    """
    Get state of smart contract

    :param contract_address: Contract address
    :param msg: Parameters to be passed to query function inside contract

    :return: JSON query response
    """
    wasm_query_client = CosmWasmQueryClient(channel)
    request = QuerySmartContractStateRequest(address=contract_address,
                                             query_data=json.dumps(msg).encode("UTF8"))
    res = wasm_query_client.SmartContractState(request)
    return json.loads(res.data)
