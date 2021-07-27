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

    def __init__(self, rest_api: QueryRestClient):
        """
        Create bank rest client

        :param rest_api: QueryRestClient api
        """
        self._rest_api = rest_api

    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        """
        Queries balance of selected denomination from specific account

        :param request: QueryBalanceRequest with address and denomination

        :return: QueryBalanceResponse
        """
        json_response = self._rest_api.get(
            self.API_URL + f"/balances/{request.address}/{request.denom}"
        )
        return Parse(json_response, QueryBalanceResponse())

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        """
        Queries balance of all denominations from specific account

        :param request: QueryAllBalancesRequest with account address

        :return: QueryAllBalancesResponse
        """
        json_response = self._rest_api.get(
            self.API_URL + f"/balances/{request.address}"
        )
        return Parse(json_response, QueryAllBalancesResponse())

    def TotalSupply(self, request: QueryTotalSupplyRequest) -> QueryTotalSupplyResponse:
        """
        Queries total supply of all denominations

        :param request: QueryTotalSupplyRequest

        :return: QueryTotalSupplyResponse
        """
        json_response = self._rest_api.get(self.API_URL + "/supply")
        return Parse(json_response, QueryTotalSupplyResponse())

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        """
        Queries total supply of specific denomination

        :param request: QuerySupplyOfRequest with denomination

        :return: QuerySupplyOfResponse
        """
        json_response = self._rest_api.get(self.API_URL + f"/supply/{request.denom}")
        return Parse(json_response, QuerySupplyOfResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Queries the parameters of bank module

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(self.API_URL + "/params")
        return Parse(json_response, QueryParamsResponse())

    def DenomMetadata(
        self, request: QueryDenomMetadataRequest
    ) -> QueryDenomMetadataResponse:
        """
        Queries the client metadata for all registered coin denominations

        :param request: QueryDenomMetadataRequest with denomination

        :return: QueryDenomMetadataResponse
        """
        json_response = self._rest_api.get(
            self.API_URL + f"/denoms_metadata/{request.denom}"
        )
        return Parse(json_response, QueryDenomMetadataResponse())

    def DenomsMetadata(
        self, request: QueryDenomsMetadataRequest
    ) -> QueryDenomsMetadataResponse:
        """
        Queries the client metadata of a given coin denomination

        :param request: QueryDenomsMetadataRequest

        :return: QueryDenomsMetadataResponse
        """
        json_response = self._rest_api.get(self.API_URL + "/denoms_metadata")
        return Parse(json_response, QueryDenomsMetadataResponse())
