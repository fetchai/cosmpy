from abc import ABC
from google.protobuf.json_format import Parse
from cosmos.bank.v1beta1.query_pb2 import (
    QueryBalanceRequest,
    QueryBalanceResponse,
    QueryAllBalancesRequest,
    QueryAllBalancesResponse,
    QueryTotalSupplyRequest,
    QueryTotalSupplyResponse,
    QuerySupplyOfRequest,
    QuerySupplyOfResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryDenomMetadataRequest,
    QueryDenomsMetadataResponse,
    QueryDenomMetadataResponse,
    QueryDenomsMetadataRequest,
)
from cosm.query.base import RestClient


class Bank(ABC):
    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        pass

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        pass

    def TotalSupply(self, request: QueryTotalSupplyRequest) -> QueryTotalSupplyResponse:
        pass

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        pass

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        pass

    def DenomMetadata(
        self, request: QueryDenomMetadataRequest
    ) -> QueryDenomMetadataResponse:
        pass

    def DenomsMetadata(
        self, request: QueryDenomsMetadataRequest
    ) -> QueryDenomsMetadataResponse:
        pass


class BankRestClient(Bank):
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        json_response = self.rest_api.query(
            f"/cosmos/bank/v1beta1/balances/{request.address}/{request.denom}"
        )
        return Parse(json_response, QueryBalanceResponse())

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        json_response = self.rest_api.query(
            f"/cosmos/bank/v1beta1/balances/{request.address}"
        )
        return Parse(json_response, QueryAllBalancesResponse())

    def TotalSupply(self, request: QueryTotalSupplyRequest) -> QueryTotalSupplyResponse:
        json_response = self.rest_api.query("/cosmos/bank/v1beta1/supply")
        return Parse(json_response, QueryTotalSupplyResponse())

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        json_response = self.rest_api.query(
            f"/cosmos/bank/v1beta1/supply/{request.denom}"
        )
        return Parse(json_response, QuerySupplyOfResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self.rest_api.query("/cosmos/bank/v1beta1/params")
        return Parse(json_response, QueryParamsResponse())

    def DenomMetadata(
        self, request: QueryDenomMetadataRequest
    ) -> QueryDenomMetadataResponse:
        json_response = self.rest_api.query(
            f"/cosmos/bank/v1beta1/denoms_metadata/{request.denom}"
        )
        return Parse(json_response, QueryDenomMetadataResponse())

    def DenomsMetadata(
        self, request: QueryDenomsMetadataRequest
    ) -> QueryDenomsMetadataResponse:
        json_response = self.rest_api.query("/cosmos/bank/v1beta1/denoms_metadata")
        return Parse(json_response, QueryDenomsMetadataResponse())
