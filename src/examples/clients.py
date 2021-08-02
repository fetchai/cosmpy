import json
import time

from typing import List
from google.protobuf.any_pb2 import Any

from common import JSONLike
from grpc import insecure_channel
from cosm.crypto.address import Address
from cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest, QueryBalanceResponse
from cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankQueryClent
from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthQueryClient
from cosmwasm.wasm.v1beta1.query_pb2_grpc import QueryStub as CosmWasmQueryClient
from cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest

from cosm.crypto.keypairs import PrivateKey
from cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmos.base.v1beta1.coin_pb2 import Coin
from cosm.tx import sign_transaction
from cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
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


class CosmWasmClient():
    def __init__(self, endpoint: str):
        """
        :param endpoint: address of gRPC endpoint
        """
        self.channel = insecure_channel(endpoint)

    def get_balance(self, address: Address, denom: str) -> QueryBalanceResponse:
        """
        Get balance of specific account and denom

        :param address: Address
        :param denom: Denomination

        :return: QueryBalanceResponse
        """
        bank_client = BankQueryClent(self.channel)
        res = bank_client.Balance(QueryBalanceRequest(address=str(address), denom=denom))
        return res

    def query_account_data(self, address: Address) -> BaseAccount:
        """
        Query account data for signing

        :param address: Address of account to query data about

        :return: BaseAccount
        """
        # Prepare clients
        auth_query_client = AuthQueryClient(self.channel)

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

    def query_contract_state(self, contract_address: str, msg: JSONLike) -> JSONLike:
        """
        Get state of smart contract

        :param contract_address: Contract address
        :param msg: Parameters to be passed to query function inside contract

        :return: JSON query response
        """
        wasm_query_client = CosmWasmQueryClient(self.channel)
        request = QuerySmartContractStateRequest(address=contract_address,
                                                 query_data=json.dumps(msg).encode("UTF8"))
        res = wasm_query_client.SmartContractState(request)
        return json.loads(res.data)


class SigningCosmWasmClient(CosmWasmClient):
    def __init__(self, private_key: PrivateKey, endpoint: str, chain_id: str):
        """
        :param private_key: Private key used for signing
        :param endpoint: address of gRPC endpoint
        :param chain_id: Chain ID
        """
        super().__init__(endpoint)

        self.private_key = private_key

        self.address = Address(self.private_key)
        account = self.query_account_data(self.address)
        self.account_number = account.account_number
        self.chain_id = chain_id

    def get_packed_send_msg(self, from_address: Address, to_address: Address, amount: List[Coin]) -> Any:
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

    def generate_tx(self, packed_msgs: List[Any], from_addresses: List[Address],
                    fee: List[Coin] = [Coin(amount="0", denom="stake")], memo: str = "", gas_limit: int = 200000) -> Tx:
        """
        Generate transaction that can be later signed

        :param packed_msgs: Messages to be in transaction
        :param from_addresses: List of addresses of each sender
        :param fee: Transaction fee
        :param memo: Memo
        :param gas_limit: Gas limit

        :return: Tx
        """

        # Get account and signer info for each sender
        accounts: List[BaseAccount] = []
        signer_infos: List[SignerInfo] = []
        for from_address in from_addresses:
            account = self.query_account_data(from_address)
            accounts.append(account)
            signer_infos.append(self._get_signer_info(account))

        # Prepare auth info
        auth_info = AuthInfo(
            signer_infos=signer_infos,
            fee=Fee(amount=fee, gas_limit=gas_limit),
        )

        # Prepare Tx body
        tx_body = TxBody()
        tx_body.memo = memo
        tx_body.messages.extend(packed_msgs)

        # Prepare Tx
        tx = Tx(body=tx_body, auth_info=auth_info)
        return tx

    def sign_tx(self, tx: Tx):
        sign_transaction(tx, self.private_key, self.chain_id, self.account_number)

    def broadcast_tx(self, tx: Tx, wait_time: int = 5) -> GetTxResponse:
        """
        Broadcast transaction and get receipt

        :param tx: Transaction
        :param wait_time: Number of seconds to wait before getting transaction receipt

        :return: GetTxResponse
        """
        tx_client = TxGrpcClient(self.channel)
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

    @staticmethod
    def _get_signer_info(self, from_acc: BaseAccount) -> SignerInfo:
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
