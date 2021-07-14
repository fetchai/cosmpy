from cosm.bank.bank_rest import BankRest
from cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from cosmos.bank.v1beta1.query_pb2 import *


class Bank:
    def __init__(self, rest_address: str):
        self.bank_api = BankRest(rest_address)

    def query_balance(self, address: str, denom: str) -> QueryBalanceResponse:
        return self.bank_api.Balance(QueryBalanceRequest(address=address, denom=denom))

    def query_all_balances(self, address: str) -> QueryAllBalancesResponse:
        return self.bank_api.AllBalances(QueryAllBalancesRequest(address=address))

    def query_total_supply(self) -> QueryTotalSupplyResponse:
        return self.bank_api.TotalSupply()

    def query_supply_of(self, denom: str) -> QuerySupplyOfResponse:
        return self.bank_api.SupplyOf(QuerySupplyOfRequest(denom=denom))

    def query_params(self) -> QueryParamsResponse:
        return self.bank_api.Params(QueryParamsRequest())

    def query_denoms_metadata(self) -> QueryDenomsMetadataResponse:
        return self.bank_api.DenomsMetadata(QueryDenomsMetadataRequest(pagination=PageRequest()))
