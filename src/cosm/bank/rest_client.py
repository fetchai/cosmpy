from google.protobuf.json_format import Parse
from cosm.query.rest_client import QueryRestClient
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

from cosm.bank.interface import Bank


class BankRestClient(Bank):
    API_URL = "/cosmos/bank/v1beta1"

    def __init__(self, rest_address: str):
        self._rest_api = QueryRestClient(rest_address)

    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        json_response = self._rest_api.get(
            self.API_URL + f"/balances/{request.address}/{request.denom}"
        )
        return Parse(json_response, QueryBalanceResponse())

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        json_response = self._rest_api.get(
            self.API_URL + f"/balances/{request.address}"
        )
        return Parse(json_response, QueryAllBalancesResponse())

    def TotalSupply(self, request: QueryTotalSupplyRequest) -> QueryTotalSupplyResponse:
        json_response = self._rest_api.get(self.API_URL + "/supply")
        return Parse(json_response, QueryTotalSupplyResponse())

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        json_response = self._rest_api.get(self.API_URL + f"/supply/{request.denom}")
        return Parse(json_response, QuerySupplyOfResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self._rest_api.get(self.API_URL + "/params")
        return Parse(json_response, QueryParamsResponse())

    def DenomMetadata(
        self, request: QueryDenomMetadataRequest
    ) -> QueryDenomMetadataResponse:
        json_response = self._rest_api.get(
            self.API_URL + f"/denoms_metadata/{request.denom}"
        )
        return Parse(json_response, QueryDenomMetadataResponse())

    def DenomsMetadata(
        self, request: QueryDenomsMetadataRequest
    ) -> QueryDenomsMetadataResponse:
        json_response = self._rest_api.get(self.API_URL + "/denoms_metadata")
        return Parse(json_response, QueryDenomsMetadataResponse())
