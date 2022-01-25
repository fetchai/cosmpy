# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of a ledger service class."""

# pylint: disable=C0302

import gzip
import json
import re
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

import requests
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.json_format import MessageToDict
from grpc import insecure_channel
from grpc._channel import Channel

from cosmpy.auth.rest_client import AuthRestClient
from cosmpy.bank.rest_client import BankRestClient
from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.common.loggers import get_logger
from cosmpy.common.rest_client import RestClient
from cosmpy.common.types import JSONLike
from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthGrpcClient
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankGrpcClient
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.protos.cosmos.crypto.secp256k1.keys_pb2 import PubKey as ProtoPubKey
from cosmpy.protos.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import (
    BroadcastMode,
    BroadcastTxRequest,
    GetTxRequest,
    GetTxResponse,
)
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2_grpc import ServiceStub as TxGrpcClient
from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import (
    AuthInfo,
    Fee,
    ModeInfo,
    SignerInfo,
    Tx,
    TxBody,
)
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QuerySmartContractStateRequest
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2_grpc import (
    QueryStub as CosmWasmGrpcClient,
)
from cosmpy.protos.cosmwasm.wasm.v1.tx_pb2 import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgStoreCode,
)
from cosmpy.tx import sign_transaction
from cosmpy.tx.rest_client import TxRestClient

_logger = get_logger(__name__)


class LedgerServerNotAvailable(Exception):
    """Ledger server is not avaiable by address provided."""


# CosmWasm client response codes
CLIENT_CODE_ERROR_EXCEPTION = 4
CLIENT_CODE_MESSAGE_SUCCESSFUL = 0

DEFAULT_GAS_LIMIT = (
    3000000  # 3000000 is the maximum gas limit - tx will fail with higher limit
)


class BroadcastException(Exception):
    """
    Broadcasting exception.
    """


# Class that provides interface to communicate with CosmWasm/Fetch blockchain
class CosmosLedger:
    """
    Implementation of a ledger service class.
    """

    _ADDR_RE = re.compile("^fetch[0-9a-z]{39}$")

    def __init__(
        self,
        chain_id: str,
        rest_node_address: Optional[str] = None,
        rpc_node_address: Optional[str] = None,
        validator_crypto: Optional[CosmosCrypto] = None,
        faucet_url: Optional[str] = None,
        msg_retry_interval: int = 2,
        msg_failed_retry_interval: int = 10,
        faucet_retry_interval: int = 20,
        n_sending_retries: int = 1,  # 5,
        n_total_msg_retries: int = 1,  # 10,
        get_response_retry_interval: float = 0.5,  # 2,
        n_get_response_retries: int = 30,  # 30,
    ):
        """
        Create new instance to deploy and communicate with smart contract

        :param chain_id: ID of a blockchain
        :param rest_node_address: web address of the REST node
        :param rpc_node_address: web address of the RPC node
        :param validator_crypto: Validator's private key - for funding from validator
        :param faucet_url: Address of testnet faucet - for funding from testnet
        :param msg_retry_interval: Interval between message partial steps retries
        :param msg_failed_retry_interval: Interval between complete send/settle message attempts
        :param faucet_retry_interval: Get wealth from faucet retry interval
        :param n_sending_retries: Number of send transaction retries
        :param n_total_msg_retries: Number of total send/settle transaction retries
        :param get_response_retry_interval: Retry interval for getting receipt
        :param n_get_response_retries: Number of get receipt retries

        :raises RuntimeError: in case of wrong configuration.
        """
        # Override presets when parameters are specified
        self.chain_id = chain_id
        self.faucet_url = faucet_url
        self.validator_crypto = validator_crypto

        # Clients to communicate with Cosmos/CosmWasm REST node

        self.rest_client: Optional[RestClient] = None
        self.rpc_client: Optional[Channel] = None

        if rest_node_address:
            self.node_address = rest_node_address
            self.rest_client = RestClient(self.node_address)
            self.tx_client: Union[TxRestClient, TxGrpcClient] = TxRestClient(
                self.rest_client
            )
            self.auth_client: Union[AuthRestClient, AuthGrpcClient] = AuthRestClient(
                self.rest_client
            )
            self.wasm_client: Union[
                CosmWasmRestClient, CosmWasmGrpcClient
            ] = CosmWasmRestClient(self.rest_client)
            self.bank_client: Union[BankRestClient, BankGrpcClient] = BankRestClient(
                self.rest_client
            )
        elif rpc_node_address:
            self.node_address = rpc_node_address
            self.rpc_client = insecure_channel(self.node_address)
            self.tx_client = TxGrpcClient(self.rpc_client)
            self.auth_client = AuthGrpcClient(self.rpc_client)
            self.wasm_client = CosmWasmGrpcClient(self.rpc_client)
            self.bank_client = BankGrpcClient(self.rpc_client)
        else:
            raise RuntimeError("No node address specified")

        self.msg_retry_interval = msg_retry_interval
        self.msg_failed_retry_interval = msg_failed_retry_interval
        self.faucet_retry_interval = faucet_retry_interval
        self.n_get_response_retries = n_get_response_retries
        self.n_sending_retries = n_sending_retries
        self.n_total_msg_retries = n_total_msg_retries
        self.get_response_retry_interval = get_response_retry_interval

    @staticmethod
    def _sleep(seconds: Union[float, int]):
        """
        Sleep n seconds

        :param seconds: Number of seconds to sleep
        """

        time.sleep(seconds)

    def deploy_contract(
        self,
        sender_crypto: CosmosCrypto,
        contract_filename: Path,
        gas: int = DEFAULT_GAS_LIMIT,
    ) -> Tuple[int, JSONLike]:
        """
        Deploy smart contract on a blockchain

        :param sender_crypto: Crypto of deployer to sign deploy transaction
        :param contract_filename: Path to contract .wasm bytecode
        :param gas:  Maximum amount of gas to be used on executing command

        :return: Deployment transaction response

        :raises BroadcastException: When communication with node fails.
        """
        attempt = 0
        res = None
        code_id: Optional[int] = None
        last_exception: Optional[Exception] = None
        while code_id is None and attempt < self.n_total_msg_retries:
            try:
                msg = self.get_packed_store_msg(
                    sender_address=sender_crypto.get_address(),
                    contract_filename=Path(contract_filename),
                )

                tx = self.generate_tx(
                    [msg],
                    [sender_crypto.get_address()],
                    [sender_crypto.get_pubkey_as_bytes()],
                    gas_limit=gas,
                )
                self.sign_tx(sender_crypto, tx)

                res = self.broadcast_tx(tx)
                code_id = self.get_code_id(res)
            except BroadcastException as e:
                # Failure due to wrong sequence, signature, etc.
                last_exception = e
                _logger.warning(
                    "Failed to deploy contract code due BroadcastException: {%s}", e
                )
                self._sleep(self.msg_failed_retry_interval)
                attempt += 1
                continue

        if code_id is None or res is None:  # pragma: nocover
            raise BroadcastException(
                f"Failed to deploy contract code after multiple attempts: {last_exception}"
            )

        return code_id, MessageToDict(res)

    @staticmethod
    def get_code_id(response: GetTxResponse) -> int:
        """
        Get code id from store code transaction response
        :param response: Response of store code transaction
        :return: integer code_id
        """
        raw_log = json.loads(response.tx_response.raw_log)
        assert raw_log[0]["events"][1]["attributes"][0]["key"] == "code_id"
        return int(raw_log[0]["events"][1]["attributes"][0]["value"])

    @staticmethod
    def get_contract_address(response: GetTxResponse) -> str:
        """
        Get contract address from instantiate msg response
        :param response: Response of MsgInstantiateContract transaction
        :return: contract address string
        """
        raw_log = json.loads(response.tx_response.raw_log)
        assert raw_log[0]["events"][0]["attributes"][0]["key"] == "_contract_address"
        return str(raw_log[0]["events"][0]["attributes"][0]["value"])

    def instantiate_contract(
        self,
        sender_crypto: CosmosCrypto,
        code_id: int,
        init_msg: JSONLike,
        label: str,
        gas: int = DEFAULT_GAS_LIMIT,
    ) -> Tuple[str, JSONLike]:
        """
        Send init contract message

        :param sender_crypto: Deployer crypto to sign init message
        :param code_id: ID of binary code stored on chain
        :param init_msg: Init message in json format
        :param label: Label of current instance of contract
        :param gas: Gas limit

        :return: Contract address string, transaction response

        :raises BroadcastException: When communication with node fails.
        """
        elapsed_time = 0
        res: Optional[GetTxResponse] = None
        contract_address: Optional[str] = None
        last_exception: Optional[Exception] = None
        while contract_address is None and elapsed_time < self.n_total_msg_retries:
            try:
                msg = self.get_packed_init_msg(
                    sender_address=sender_crypto.get_address(),
                    code_id=code_id,
                    init_msg=init_msg,
                    label=label,
                )

                tx = self.generate_tx(
                    [msg],
                    [sender_crypto.get_address()],
                    [sender_crypto.get_pubkey_as_bytes()],
                    gas_limit=gas,
                )
                self.sign_tx(sender_crypto, tx)

                res = self.broadcast_tx(tx)
                contract_address = self.get_contract_address(res)

            except BroadcastException as e:
                # Failure due to wrong sequence, signature, etc.
                last_exception = e
                _logger.warning(
                    "Failed to init contract due BroadcastException: {%s}", e
                )
            except json.decoder.JSONDecodeError as e:
                # Failure due to response parsing error
                last_exception = e
                _logger.warning(
                    "Failed to parse init Contract response {%s} : {%s}",
                    res.tx_response.raw_log if res is not None else None,
                    e,
                )

            if contract_address is None:
                self._sleep(self.msg_failed_retry_interval)
                elapsed_time += 1

        if contract_address is None or res is None:
            error_msg = ""
            if res:
                error_msg = res.tx_response.raw_log

            raise BroadcastException(
                f"Failed to init contract after multiple attempts: {last_exception} {error_msg}"
            )

        return contract_address, MessageToDict(res)

    def query_contract_state(
        self,
        contract_address: str,
        msg: JSONLike,
        num_retries: Optional[int] = None,
    ) -> JSONLike:
        """
        Generate and send query message to get state of smart contract
        - No signing is required because it works with contract as read only

        :param contract_address: Address of contract running on chain
        :param msg: Query message in json format
        :param num_retries: Optional number of retries

        :return: Query json response

        :raises BroadcastException: When communication with node fails.
        """
        request = QuerySmartContractStateRequest(
            address=contract_address, query_data=json.dumps(msg).encode("UTF8")
        )

        if num_retries is None:
            num_retries = self.n_total_msg_retries

        res = None
        last_exception: Optional[Exception] = None
        for _ in range(num_retries):
            try:
                res = self.wasm_client.SmartContractState(request)
                if res is not None:
                    break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                _logger.warning("Cannot get contract state: {%s}", e)
                self._sleep(self.msg_failed_retry_interval)

        if res is None:
            raise BroadcastException(
                f"Getting contract state failed after multiple attempts: {last_exception}"
            ) from last_exception
        return json.loads(res.data)  # pylint: disable=E1101

    def execute_contract(
        self,
        sender_crypto: CosmosCrypto,
        contract_address: str,
        execute_msg: JSONLike,
        gas: int = DEFAULT_GAS_LIMIT,
        amount: Optional[List[Coin]] = None,
        retries: Optional[int] = None,
    ) -> Tuple[JSONLike, int]:
        """
        Generate, sign and send handle message

        :param sender_crypto: Sender's crypto to sign init message
        :param contract_address: Address of contract running on chain
        :param execute_msg: Execute message in json format
        :param gas: Gas limit
        :param amount: Funds to be transferred to contract address
        :param retries: Optional number of retries

        :raises BroadcastException: When communication with node fails.

        :return: Execute message response
        """
        res: Optional[GetTxResponse] = None
        last_exception: Optional[Exception] = None

        if retries is None:
            retries = self.n_sending_retries

        for _ in range(retries):
            try:

                msg = self.get_packed_exec_msg(
                    sender_address=sender_crypto.get_address(),
                    contract_address=contract_address,
                    msg=execute_msg,
                    funds=amount,
                )

                tx = self.generate_tx(
                    [msg],
                    [sender_crypto.get_address()],
                    [sender_crypto.get_pubkey_as_bytes()],
                    gas_limit=gas,
                )
                self.sign_tx(sender_crypto, tx)
                res = self.broadcast_tx(tx)
                if res is not None:
                    break
            except BroadcastException as e:
                # Failure due to wrong sequence, signature, etc.
                last_exception = e
                _logger.warning(
                    "Failed to deploy contract code due BroadcastException: {%s}", e
                )
                self._sleep(self.msg_failed_retry_interval)

        if res is None:
            raise BroadcastException(
                f"Failed to execute contract after multiple attempts: {last_exception}"
            ) from last_exception

        # err_code >0 in case of exceptions inside rust contract
        err_code = res.tx_response.code  # pylint: disable=E1101
        return MessageToDict(res), err_code

    def get_balance(self, address: str, denom: str) -> int:
        """
        Query funds of address and denom

        :param address: Address to be query
        :param denom: Denom of coins

        :return: Integer representation of amount

        :raises BroadcastException: When communication with node fails.
        """

        res = None
        last_exception: Optional[Exception] = None
        for _ in range(self.n_total_msg_retries):
            try:
                res = self.bank_client.Balance(
                    QueryBalanceRequest(address=str(address), denom=denom)
                )
                if res is not None:
                    break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                _logger.warning("Cannot get balance: {%s}", e)
                self._sleep(self.msg_retry_interval)
                continue

        if res is None:
            raise BroadcastException(
                f"Getting balance failed after multiple attempts: {last_exception}"
            )

        return int(res.balance.amount)

    def get_balances(self, address: str) -> List[Coin]:
        """
        Query all funds of address

        :param address: Address to be query

        :raises BroadcastException: When communication with node fails.

        :return: List of coins
        """

        res = None
        last_exception: Optional[Exception] = None
        for _ in range(self.n_total_msg_retries):
            try:
                res = self.bank_client.AllBalances(
                    QueryBalanceRequest(address=str(address))
                )
                if res is not None:
                    break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                _logger.warning("Cannot get balances: {%s}", e)
                self._sleep(self.msg_retry_interval)
                continue

        if res is None:
            raise BroadcastException(
                f"Getting balances failed after multiple attempts: {last_exception}"
            )

        return res.balances

    def refill_wealth_from_faucet(
        self, addresses: List[str], amount: Optional[int] = None
    ):
        """
        Uses faucet api to refill balance of addresses

        :param addresses: List of addresses to be refilled
        :param amount: Required amount
        """

        min_amount_required = amount if amount else 500000000

        for address in addresses:
            attempts_allowed = 10

            # Retry in case of network issues
            while attempts_allowed > 0:
                try:
                    attempts_allowed -= 1

                    # Get balance of first available coin
                    balances = self.get_balances(address)
                    if balances:
                        balance = int(balances[0].amount)
                    else:
                        balance = 0

                    if balance < min_amount_required:
                        _logger.info(
                            "Refilling balance of {%s} from faucet. Currently: {%s}",
                            address,
                            balance,
                        )
                        # Send faucet request
                        response = requests.post(
                            f"{self.faucet_url}/api/v3/claims",
                            json={"address": address},
                        )

                        if response.status_code != 200:
                            _logger.exception(
                                "Failed to refill the balance from faucet, retry in {%s} seconds: {%s}",
                                self.faucet_retry_interval,
                                str(response),
                            )

                        # Wait for wealth to be refilled
                        self._sleep(self.faucet_retry_interval)
                        continue
                    _logger.info("Balance of {%s} is {%s}", address, balance)
                    break
                except Exception as e:  # pylint: disable=W0703
                    _logger.exception(
                        "Failed to refill the balance from faucet, retry in {%s} second: {%s} ({%s})",
                        self.faucet_retry_interval,
                        e,
                        type(e),
                    )
                    self._sleep(self.faucet_retry_interval)
                    continue

    def send_funds(
        self,
        from_crypto: CosmosCrypto,
        to_address: str,
        amount_coins: List[Coin],
    ):
        """
        Transfer funds from one address to another address

        :param from_crypto: Crypto with funds to be sent
        :param to_address: Address to receive funds
        :param amount_coins: List of coins to be sent

        :return: Transaction response
        """

        from_address = str(from_crypto.get_address())

        msg = self.get_packed_send_msg(
            from_address=from_address, to_address=to_address, amount=amount_coins
        )

        tx = self.generate_tx(
            [msg], [from_address], [from_crypto.get_pubkey_as_bytes()]
        )
        self.sign_tx(from_crypto, tx)

        return self.broadcast_tx(tx)

    def sign_tx(self, crypto: CosmosCrypto, tx: Tx):
        """
        Sign tx using crypto
        - network is used to query account_number if not already stored in crypto

        :param crypto: Crypto used to sign transaction
        :param tx: Transaction to be signed

        :raises RuntimeError: When getting account number fails.
        """

        # Update account number if needed - Getting account data might fail if address is not funded
        self._ensure_accont_number(crypto)

        if crypto.account_number is None:
            raise RuntimeError("Getting account number failed")

        sign_transaction(tx, crypto.private_key, self.chain_id, crypto.account_number)

    def _ensure_accont_number(self, crypto: CosmosCrypto):
        if crypto.account_number is None:
            account = self.query_account_data(crypto.get_address())
            crypto.account_number = account.account_number  # pylint: disable=E1101

    def ensure_funds(
        self, addresses: List[str], amount_coins: Optional[List[Coin]] = None
    ):
        """
        Refill funds of addresses using faucet or validator
        :param addresses: Address to be refilled
        :param amount_coins: Amount of refill

        :raises RuntimeError: When parameters are missing.
        """

        if self.faucet_url is not None:
            self.refill_wealth_from_faucet(addresses)
        elif self.validator_crypto is not None:
            if amount_coins is None:
                raise RuntimeError("Amounts are required for validator refill")
            self.refill_wealth_from_validator(
                self.validator_crypto, addresses, amount_coins
            )
        else:
            raise RuntimeError(
                "Faucet or validator was not specified, cannot refill addresses"
            )

    def refill_wealth_from_validator(
        self,
        validator_crypto: CosmosCrypto,
        addresses: List[str],
        required_amount_coins: List[Coin],
    ):
        """
        Refill funds of addresses using validator
        - Works only for local-net with validator account

        :param validator_crypto: Validator crypto
        :param addresses: Addresses to be refilled
        :param required_amount_coins: Required amounts of coins
        """

        for address in addresses:
            # balances = self.get_balances(address)

            # Subtract coins
            amount_coins = required_amount_coins

            self.send_funds(validator_crypto, address, amount_coins)

    def generate_tx(
        self,
        packed_msgs: List[ProtoAny],
        from_addresses: List[str],
        pub_keys: List[bytes],
        fee: Optional[List[Coin]] = None,
        memo: str = "",
        gas_limit: int = DEFAULT_GAS_LIMIT,
    ) -> Tx:
        """
        Generate transaction that can be later signed

        :param packed_msgs: Messages to be in transaction
        :param from_addresses: List of addresses of each sender
        :param pub_keys: List of public keys
        :param fee: Transaction fee
        :param memo: Memo
        :param gas_limit: Gas limit

        :return: Tx
        """

        # Get account and signer info for each sender
        accounts: List[BaseAccount] = []
        signer_infos: List[SignerInfo] = []
        for from_address, pub_key in zip(from_addresses, pub_keys):
            account = self.query_account_data(from_address)
            accounts.append(account)
            signer_infos.append(self._get_signer_info(account, pub_key))

        # Prepare auth info
        auth_info = AuthInfo(
            signer_infos=signer_infos,
            fee=Fee(amount=fee, gas_limit=gas_limit),
        )

        # Prepare Tx body
        tx_body = TxBody()
        tx_body.memo = memo
        tx_body.messages.extend(packed_msgs)  # pylint: disable=E1101

        # Prepare Tx
        tx = Tx(body=tx_body, auth_info=auth_info)
        return tx

    def query_account_data(self, address: str) -> BaseAccount:
        """
        Query account data for signing

        :param address: Address of account to query data about

        :raises TypeError: in case of wrong account type.
        :raises BroadcastException: if broadcasting fails.

        :return: BaseAccount
        """
        # Get account data for signing

        last_exception: Optional[Exception] = None
        account_response = None
        for _ in range(self.n_total_msg_retries):
            try:
                account_response = self.auth_client.Account(
                    QueryAccountRequest(address=str(address))
                )
                break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                _logger.warning("Cannot query account data: {%s}", e)
                self._sleep(self.msg_retry_interval)
                continue

        if account_response is None:
            raise BroadcastException(
                f"Getting account data failed after multiple attempts: {last_exception}"
            )

        account = BaseAccount()
        if account_response.account.Is(BaseAccount.DESCRIPTOR):
            account_response.account.Unpack(account)
        else:
            raise TypeError("Unexpected account type")
        return account

    @staticmethod
    def _get_signer_info(from_acc: BaseAccount, pub_key: bytes) -> SignerInfo:
        """
        Generate signer info

        :param from_acc: Account info of signer
        :param pub_key: Public key bytes

        :return: SignerInfo
        """

        from_pub_key_packed = ProtoAny()
        from_pub_key_pb = ProtoPubKey(key=pub_key)
        from_pub_key_packed.Pack(from_pub_key_pb, type_url_prefix="/")  # type: ignore

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
    def get_packed_send_msg(
        from_address: str, to_address: str, amount: List[Coin]
    ) -> ProtoAny:
        """
        Generate and pack MsgSend

        :param from_address: Address of sender
        :param to_address: Address of recipient
        :param amount: List of Coins to be sent

        :return: packer ProtoAny type message
        """
        msg_send = MsgSend(
            from_address=str(from_address), to_address=str(to_address), amount=amount
        )
        send_msg_packed = ProtoAny()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")  # type: ignore

        return send_msg_packed

    def broadcast_tx(self, tx: Tx, retries: Optional[int] = None) -> GetTxResponse:
        """
        Broadcast transaction and get receipt

        :param tx: Transaction
        :param retries: Optional number of broadcasting attempts

        :raises BroadcastException: if broadcasting fails.

        :return: GetTxResponse
        """

        tx_data = tx.SerializeToString()
        broad_tx_req = BroadcastTxRequest(
            tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        if retries is None:
            retries = self.n_total_msg_retries

        last_exception = None
        broad_tx_resp = None
        for _ in range(retries):
            try:
                broad_tx_resp = self.tx_client.BroadcastTx(broad_tx_req)
                break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                _logger.warning("Transaction broadcasting failed: {%s}", e)
                self._sleep(self.msg_retry_interval)

        if broad_tx_resp is None:
            raise BroadcastException(
                f"Broadcasting tx failed after multiple attempts: {last_exception}"
            )

        # Transaction cannot be broadcast because of wrong format, sequence, signature, etc.
        if broad_tx_resp.tx_response.code != CLIENT_CODE_MESSAGE_SUCCESSFUL:
            raw_log = broad_tx_resp.tx_response.raw_log
            raise BroadcastException(f"Transaction cannot be broadcast: {raw_log}")

        # Wait for transaction to settle
        return self.get_tx(txhash=broad_tx_resp.tx_response.txhash)

    def get_tx(self, txhash) -> GetTxResponse:
        """
        Get transaction receipt

        :param txhash: TX hash of the transaction

        :raises BroadcastException: if getting tx receipt fails.

        :return: GetTxResponse
        """

        tx_request = GetTxRequest(hash=txhash)
        last_exception = None
        tx_response = None

        for _ in range(self.n_get_response_retries):
            try:
                # Send GetTx request
                tx_response = self.tx_client.GetTx(tx_request)
                break
            except Exception as e:  # pylint: disable=W0703
                # This fails when Tx is not on chain yet - not an actual error
                last_exception = e
                self._sleep(self.get_response_retry_interval)
                continue

        if tx_response is None:
            raise BroadcastException(
                f"Getting tx response failed after multiple attempts: {last_exception}"
            ) from last_exception

        return tx_response

    @staticmethod
    def get_packed_store_msg(sender_address: str, contract_filename: Path) -> ProtoAny:
        """
        Loads contract bytecode, generate and return packed MsgStoreCode

        :param sender_address: Address of transaction sender
        :param contract_filename: Path to smart contract bytecode

        :return: Packed MsgStoreCode
        """
        with open(contract_filename, "rb") as contract_file:
            wasm_byte_code = gzip.compress(contract_file.read(), 9)

        msg_send = MsgStoreCode(
            sender=str(sender_address),
            wasm_byte_code=wasm_byte_code,
        )
        send_msg_packed = ProtoAny()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")  # type: ignore

        return send_msg_packed

    @staticmethod
    def get_packed_init_msg(
        sender_address: str,
        code_id: int,
        init_msg: JSONLike,
        label="contract",
        funds: Optional[List[Coin]] = None,
    ) -> ProtoAny:
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
            msg=json.dumps(init_msg).encode("UTF8"),
            label=label,
            funds=funds,
        )
        send_msg_packed = ProtoAny()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")  # type: ignore

        return send_msg_packed

    @staticmethod
    def get_packed_exec_msg(
        sender_address: str,
        contract_address: str,
        msg: JSONLike,
        funds: Optional[List[Coin]] = None,
    ) -> ProtoAny:
        """
        Create and pack MsgExecuteContract

        :param sender_address: Address of sender
        :param contract_address: Address of contract
        :param msg: Parameters to be passed to smart contract
        :param funds: Funds to be sent to smart contract

        :return: Packed MsgExecuteContract
        """
        msg_send = MsgExecuteContract(
            sender=str(sender_address),
            contract=contract_address,
            msg=json.dumps(msg).encode("UTF8"),
            funds=funds,
        )
        send_msg_packed = ProtoAny()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")  # type: ignore

        return send_msg_packed

    def check_availability(self):
        """
        Check node availability

        :raises ValueError: When bad chain ID.
        :raises LedgerServerNotAvailable: When ledger server is not available.
        :raises NotImplementedError for RPC node
        """

        if self.rest_client:
            try:
                result = json.loads(self.rest_client.get("/node_info"))
                if result["node_info"]["network"] != self.chain_id:
                    raise ValueError("Bad chain id")
            except Exception as e:
                raise LedgerServerNotAvailable(
                    f"ledger server is not available with address: {self.node_address}: {e}"
                ) from e
        else:
            raise NotImplementedError(
                "Checking availability of RPC node not implemented yet"
            )

    @classmethod
    def validate_address(cls, address: str):
        """
        Check if given address is in correct format

        :param address: Address to be checked

        :raises ValueError: if address is in wrong format.
        """

        if not cls._ADDR_RE.match(address):
            raise ValueError(f"Address {address} is invalid")
