from cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest, QueryBalanceResponse, QueryAllBalancesRequest, \
    QueryAllBalancesResponse, QueryTotalSupplyRequest, QueryTotalSupplyResponse, QuerySupplyOfRequest, \
    QuerySupplyOfResponse, QueryParamsRequest, QueryParamsResponse, QueryDenomMetadataRequest, \
    QueryDenomsMetadataResponse, QueryDenomMetadataResponse, QueryDenomsMetadataRequest


class Bank:
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

    def DenomMetadata(self, request: QueryDenomMetadataRequest) -> QueryDenomMetadataResponse:
        pass

    def DenomsMetadata(self, request: QueryDenomsMetadataRequest) -> QueryDenomsMetadataResponse:
        pass
