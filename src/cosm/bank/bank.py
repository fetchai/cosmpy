from cosmos.bank.v1beta1.query_pb2 import *


class Bank:
    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        pass

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        pass

    def TotalSupply(self) -> QueryTotalSupplyResponse:
        pass

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        pass

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        pass

    def DenomMetadata(self, request: QueryDenomMetadataRequest) -> QueryDenomMetadataResponse:
        pass

    def DenomsMetadata(self, request: QueryDenomsMetadataRequest) -> QueryDenomsMetadataResponse:
        pass
