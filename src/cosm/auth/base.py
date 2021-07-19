from abc import ABC
from google.protobuf.json_format import Parse
from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)
from cosm.query.base import RestClient


class Auth(ABC):
    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        pass

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        pass


class AuthRestClient(Auth):
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        json_response = self.rest_api.query(
            f"/cosmos/auth/v1beta1/accounts/{request.address}"
        )
        return Parse(json_response, QueryAccountResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self.rest_api.query("/cosmos/auth/v1beta1/params")
        return Parse(json_response, QueryParamsResponse())
