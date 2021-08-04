from abc import ABC, abstractmethod

from cosmos.bank.v1beta1.query_pb2 import (
    QueryAllBalancesRequest,
    QueryAllBalancesResponse,
    QueryBalanceRequest,
    QueryBalanceResponse,
    QueryDenomMetadataRequest,
    QueryDenomMetadataResponse,
    QueryDenomsMetadataRequest,
    QueryDenomsMetadataResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QuerySupplyOfRequest,
    QuerySupplyOfResponse,
    QueryTotalSupplyRequest,
    QueryTotalSupplyResponse,
)


class Bank(ABC):
    @abstractmethod
    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        """
        Queries balance of selected denomination from specific account

        :param request: QueryBalanceRequest with address and denomination

        :return: QueryBalanceResponse
        """
        ...

    @abstractmethod
    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        """
        Queries balance of all denominations from specific account

        :param request: QueryAllBalancesRequest with account address

        :return: QueryAllBalancesResponse
        """
        ...

    @abstractmethod
    def TotalSupply(self, request: QueryTotalSupplyRequest) -> QueryTotalSupplyResponse:
        """
        Queries total supply of all denominations

        :param request: QueryTotalSupplyRequest

        :return: QueryTotalSupplyResponse
        """
        ...

    @abstractmethod
    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        """
        Queries total supply of specific denomination

        :param request: QuerySupplyOfRequest with denomination

        :return: QuerySupplyOfResponse
        """
        ...

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Queries the parameters of bank module

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        ...

    @abstractmethod
    def DenomMetadata(
        self, request: QueryDenomMetadataRequest
    ) -> QueryDenomMetadataResponse:
        """
        Queries the client metadata for all registered coin denominations

        :param request: QueryDenomMetadataRequest with denomination

        :return: QueryDenomMetadataResponse
        """
        ...

    @abstractmethod
    def DenomsMetadata(
        self, request: QueryDenomsMetadataRequest
    ) -> QueryDenomsMetadataResponse:
        """
        Queries the client metadata of a given coin denomination

        :param request: QueryDenomsMetadataRequest

        :return: QueryDenomsMetadataResponse
        """
        ...
