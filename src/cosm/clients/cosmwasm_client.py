import json
from typing import Union

from grpc._channel import Channel

from common import JSONLike
from cosm.auth.rest_client import AuthRestClient
from cosm.bank.rest_client import BankRestClient
from cosm.crypto.address import Address
from cosm.query.rest_client import QueryRestClient
from cosm.wasm.rest_client import WasmRestClient
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthGrpcClient
from cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest, QueryBalanceResponse
from cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankGrpcClient
from cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest
from cosmwasm.wasm.v1beta1.query_pb2_grpc import QueryStub as CosmWasmGrpcClient


class CosmWasmClient:
    def __init__(self, channel: Union[Channel, QueryRestClient]):
        """
        :param channel: gRPC or REST querying client

        :raises RuntimeError: if channel is of wrong type.
        """

        if isinstance(channel, Channel):
            self.bank_client = BankGrpcClient(channel)
            self.auth_client = AuthGrpcClient(channel)
            self.wasm_client = CosmWasmGrpcClient(channel)
        elif isinstance(channel, QueryRestClient):
            self.bank_client = BankRestClient(channel)
            self.auth_client = AuthRestClient(channel)
            self.wasm_client = WasmRestClient(channel)
        else:
            raise RuntimeError(f"Unsupported channel type {type(channel)}")

    def get_balance(self, address: Address, denom: str) -> QueryBalanceResponse:
        """
        Get balance of specific account and denom

        :param address: Address
        :param denom: Denomination

        :return: QueryBalanceResponse
        """
        res = self.bank_client.Balance(
            QueryBalanceRequest(address=str(address), denom=denom)
        )
        return res

    def query_account_data(self, address: Address) -> BaseAccount:
        """
        Query account data for signing

        :param address: Address of account to query data about

        :raises TypeError: in case of wrong account type.

        :return: BaseAccount
        """
        # Get account data for signing
        account_response = self.auth_client.Account(
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
        request = QuerySmartContractStateRequest(
            address=contract_address, query_data=json.dumps(msg).encode("UTF8")
        )
        res = self.wasm_client.SmartContractState(request)
        return json.loads(res.data)
