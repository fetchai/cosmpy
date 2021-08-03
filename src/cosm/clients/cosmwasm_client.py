import json

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


class CosmWasmClient:
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
        res = bank_client.Balance(
            QueryBalanceRequest(address=str(address), denom=denom)
        )
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
        request = QuerySmartContractStateRequest(
            address=contract_address, query_data=json.dumps(msg).encode("UTF8")
        )
        res = wasm_query_client.SmartContractState(request)
        return json.loads(res.data)
