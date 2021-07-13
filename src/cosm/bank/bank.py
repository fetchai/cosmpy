from cosm.query.rest_client import RestClient
from common import JSONLike
from cosmos.bank.v1beta1.query_pb2 import QueryBalanceResponse, QueryBalanceRequest, QueryAllBalancesRequest, \
    QueryAllBalancesResponse, QueryTotalSupplyResponse, QuerySupplyOfRequest, QuerySupplyOfResponse, \
    QueryDenomMetadataRequest, QueryDenomMetadataResponse, QueryDenomsMetadataRequest, QueryDenomsMetadataResponse
from cosmos.bank.v1beta1.bank_pb2 import Metadata

from cosmos.base.query.v1beta1.pagination_pb2 import PageRequest, PageResponse

from cosmos.base.v1beta1.coin_pb2 import Coin


class Bank:
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def query_balance(self, address: str, denom: str) -> QueryBalanceResponse:
        return self._query_balance(QueryBalanceRequest(address=address, denom=denom))

    def query_all_balances(self, address: str) -> QueryAllBalancesResponse:
        return self._query_all_balances(QueryAllBalancesRequest(address=address))

    def query_total_supply(self) -> QueryTotalSupplyResponse:
        return self._query_total_supply()

    def query_supply_of(self, denom: str) -> QuerySupplyOfResponse:
        return self._query_supply_of(QuerySupplyOfRequest(denom=denom))

    def query_denoms_metadata(self) -> QueryDenomsMetadataResponse:
        return self._query_denoms_metadata(QueryDenomsMetadataRequest(pagination=PageRequest()))

    def query_denom_metadata(self, denom: str) -> QueryDenomMetadataResponse:
        return self._query_denom_metadata(QueryDenomMetadataRequest(denom=denom))

    @staticmethod
    def _convert_to_list_of_coins(json_response: JSONLike) -> [Coin]:
        res: [Coin] = []
        for coin in json_response:
            res.append(Coin(denom=coin["denom"],
                            amount=coin["amount"]))
        return res

    def _query_balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}/{request.denom}")

        return QueryBalanceResponse(
            balance=Coin(denom=json_response["balance"]["denom"],
                         amount=json_response["balance"]["amount"]))

    def _query_all_balances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}")

        pagination = PageResponse(next_key=json_response["pagination"]["next_key"],
                                  total=int(json_response["pagination"]["total"]))

        return QueryAllBalancesResponse(
            balances=self._convert_to_list_of_coins(json_response["balances"]),
            pagination=pagination)

    def _query_total_supply(self) -> QueryTotalSupplyResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply")
        return QueryTotalSupplyResponse(supply=self._convert_to_list_of_coins(json_response["supply"]))

    def _query_supply_of(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply/{request.denom}")

        return QuerySupplyOfResponse(
            amount=Coin(denom=json_response["amount"]["denom"],
                        amount=json_response["amount"]["amount"]))

    def _query_denoms_metadata(self, request: QueryDenomsMetadataRequest) -> QueryDenomsMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata")

        pagination = PageResponse(next_key=json_response["pagination"]["next_key"],
                                  total=int(json_response["pagination"]["total"]))

        metadatas: [Metadata] = []
        for metadata in json_response["metadatas"]:
            metadatas.append(Metadata(metadata))

        return QueryDenomsMetadataResponse(metadatas=metadatas, pagination=pagination)

    def _query_denom_metadata(self, request: QueryDenomMetadataRequest) -> QueryDenomMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata/{request.denom}")

        return QueryDenomsMetadataResponse(metadata=Metadata(json_response["metadata"]))
