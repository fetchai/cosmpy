from cosm.query.rest_client import RestClient

from cosmos.bank.v1beta1.query_pb2 import *
from google.protobuf.json_format import Parse
from cosmos.base.query.v1beta1.pagination_pb2 import PageRequest


class Bank:
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def query_balance(self, address: str, denom: str) -> QueryBalanceResponse:
        return self.Balance(QueryBalanceRequest(address=address, denom=denom))

    def query_all_balances(self, address: str) -> QueryAllBalancesResponse:
        return self.AllBalances(QueryAllBalancesRequest(address=address))

    def query_total_supply(self) -> QueryTotalSupplyResponse:
        return self.TotalSupply()

    def query_supply_of(self, denom: str) -> QuerySupplyOfResponse:
        return self.SupplyOf(QuerySupplyOfRequest(denom=denom))

    def query_params(self) -> QueryParamsResponse:
        return self.Params(QueryParamsRequest())

    def query_denoms_metadata(self) -> QueryDenomsMetadataResponse:
        return self.DenomsMetadata(QueryDenomsMetadataRequest(pagination=PageRequest()))

    def query_denom_metadata(self, denom: str) -> QueryDenomMetadataResponse:
        return self.DenomMetadata(QueryDenomMetadataRequest(denom=denom))

    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}/{request.denom}")
        return Parse(json_response, QueryBalanceResponse())

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}")
        return Parse(json_response, QueryAllBalancesResponse())

    def TotalSupply(self) -> QueryTotalSupplyResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply")
        return Parse(json_response, QueryTotalSupplyResponse())

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply/{request.denom}")
        return Parse(json_response, QuerySupplyOfResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/params")
        return Parse(json_response, QueryDenomsMetadataResponse())

    def DenomMetadata(self, request: QueryDenomsMetadataRequest) -> QueryDenomsMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata")
        return Parse(json_response, QueryDenomsMetadataResponse())

    def DenomsMetadata(self, request: QueryDenomMetadataRequest) -> QueryDenomMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata/{request.denom}")
        return Parse(json_response, QueryDenomsMetadataResponse())
