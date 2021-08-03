import gzip
import json
import time
from pathlib import Path

from typing import List
from google.protobuf.any_pb2 import Any

from common import JSONLike
from cosm.crypto.address import Address
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount

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
from cosmos.tx.v1beta1.service_pb2 import (
    BroadcastTxRequest,
    BroadcastMode,
    GetTxRequest,
    GetTxResponse,
)
from cosmwasm.wasm.v1beta1.tx_pb2 import (
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
)
from cosm.clients.cosmwasm_client import CosmWasmClient


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

    def generate_tx(
        self,
        packed_msgs: List[Any],
        from_addresses: List[Address],
        fee: List[Coin] = [Coin(amount="0", denom="stake")],
        memo: str = "",
        gas_limit: int = 200000,
    ) -> Tx:
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
        """
        Sign transaction

        :param tx: Transaction to be signed
        """
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
    def get_packed_send_msg(
        from_address: Address, to_address: Address, amount: List[Coin]
    ) -> Any:
        """
        Generate and pack MsgSend

        :param from_address: Address of sender
        :param to_address: Address of recipient
        :param amount: List of Coins to be sent

        :return: packer Any type message
        """
        msg_send = MsgSend(
            from_address=str(from_address), to_address=str(to_address), amount=amount
        )
        send_msg_packed = Any()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")

        return send_msg_packed

    @staticmethod
    def get_packed_store_msg(sender_address: Address, contract_filename: Path) -> Any:
        """
        Loads contract bytecode, generate and return packed MsgStoreCode

        :param sender_address: Address of transaction sender
        :param contract_filename: Path to smart contract bytecode

        :return: Packed MsgStoreCode
        """
        with open(contract_filename, "rb") as contract_file:
            wasm_byte_code = gzip.compress(contract_file.read(), 6)

        msg_send = MsgStoreCode(
            sender=str(sender_address),
            wasm_byte_code=wasm_byte_code,
        )
        send_msg_packed = Any()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")

        return send_msg_packed

    @staticmethod
    def get_packed_init_msg(
        sender_address: Address,
        code_id: int,
        init_msg: JSONLike,
        label="contract",
        funds: List[Coin] = [],
    ) -> Any:
        """
        Create and pack MsgInstantiateContract

        :param sender_address: Sender's address
        :param code_id: code_id of stored contract bytecode
        :param init_msg: Parameters to be passed to smart contract constructor
        :param label: Label
        :param funds: Funds transferred to new contract

        :return: Packed MsgInstantiateContract
        """
        msg_send = MsgInstantiateContract(
            sender=str(sender_address),
            code_id=code_id,
            init_msg=json.dumps(init_msg).encode("UTF8"),
            label=label,
            funds=funds,
        )
        send_msg_packed = Any()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")

        return send_msg_packed

    @staticmethod
    def get_packed_exec_msg(
        sender_address: Address,
        contract_address: str,
        msg: JSONLike,
        funds: List[Coin] = [],
    ) -> Any:
        """
        Create and pack MsgExecuteContract

        :param sender_address: Address of sender
        :param contract_address: Address of contract
        :param msg: Paramaters to be passed to smart contract
        :param funds: Funds to be sent to smart contract

        :return: Packed MsgExecuteContract
        """
        msg_send = MsgExecuteContract(
            sender=str(sender_address),
            contract=contract_address,
            msg=json.dumps(msg).encode("UTF8"),
            funds=funds,
        )
        send_msg_packed = Any()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")

        return send_msg_packed

    # Higher level methods
    def send_tokens(self, to_address: Address, amount: List[Coin]) -> GetTxResponse:
        """
        Send native tokens from clients address to to_address

        :param to_address: Address of recipient
        :param amount: List of tokens to be transferred

        :return: GetTxResponse
        """
        msg = self.get_packed_send_msg(
            from_address=self.address, to_address=to_address, amount=amount
        )

        tx = self.generate_tx([msg], [self.address])
        self.sign_tx(tx)
        return self.broadcast_tx(tx)

    def store_contract(self, contract_filename: Path, gas_limit: int = 2000000) -> int:
        """
        Deploy smart contract on chain

        :param contract_filename: Path to smart contract bytecode
        :param gas_limit: Gas limit

        :return: Code ID
        """
        msg = self.get_packed_store_msg(
            sender_address=self.address, contract_filename=contract_filename
        )

        tx = self.generate_tx([msg], [self.address], gas_limit=gas_limit)
        self.sign_tx(tx)
        res = self.broadcast_tx(tx)
        return self._get_code_id(res)

    def instantiate(
        self,
        code_id: int,
        init_msg: JSONLike,
        label="contract",
        funds: List[Coin] = [],
        gas_limit: int = 200000,
    ) -> GetTxResponse:
        """
        Instantiate smart contract and return contract address

        :param code_id: code_id of stored contract bytecode
        :param init_msg: Parameters to be passed to smart contract constructor
        :param label: Label
        :param funds: Funds transferred to new contract
        :param gas_limit: Gas limit

        :return: Contract address
        """
        msg = self.get_packed_init_msg(
            sender_address=self.address,
            code_id=code_id,
            init_msg=init_msg,
            label=label,
            funds=funds,
        )

        tx = self.generate_tx([msg], [self.address], gas_limit=gas_limit)
        self.sign_tx(tx)
        res = self.broadcast_tx(tx)
        return self._get_contract_address(res)

    def execute(
        self,
        contract_address: str,
        msg: JSONLike,
        funds: List[Coin] = [],
        gas_limit: int = 200000,
    ) -> GetTxResponse:
        """
        Send execute message to interact with smart contract

        :param contract_address: Address of contract
        :param msg: Paramaters to be passed to smart contract
        :param funds: Funds to be sent to smart contract
        :param gas_limit: Gas limit

        :return: GetTxResponse
        """
        msg = self.get_packed_exec_msg(
            sender_address=self.address,
            contract_address=contract_address,
            msg=msg,
            funds=funds,
        )

        tx = self.generate_tx([msg], [self.address], gas_limit=gas_limit)
        self.sign_tx(tx)
        return self.broadcast_tx(tx)

    # Protected attributes
    @staticmethod
    def _get_signer_info(from_acc: BaseAccount) -> SignerInfo:
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

    @staticmethod
    def _get_code_id(response: GetTxResponse) -> int:
        """
        Get code id from store code transaction response

        :param response: Response of store code transaction

        :return: integer code_id
        """
        raw_log = json.loads(response.tx_response.raw_log)
        assert raw_log[0]["events"][0]["attributes"][3]["key"] == "code_id"
        return int(raw_log[0]["events"][0]["attributes"][3]["value"])

    @staticmethod
    def _get_contract_address(response: GetTxResponse) -> str:
        """
        Get contract address from instantiate msg response
        :param response: Response of MsgInstantiateContract transaction

        :return: contract address string
        """
        raw_log = json.loads(response.tx_response.raw_log)
        assert raw_log[0]["events"][1]["attributes"][0]["key"] == "contract_address"
        return str(raw_log[0]["events"][1]["attributes"][0]["value"])
