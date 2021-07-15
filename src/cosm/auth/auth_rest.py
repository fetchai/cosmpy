from cosm.query.rest_client import RestClient
from cosm.auth.auth import Auth

from cosmos.auth.v1beta1.query_pb2 import *
from google.protobuf.json_format import Parse


class AuthRest(Auth):
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        json_response = self.rest_api.query(f"/cosmos/auth/v1beta1/accounts/{request.address}")
        return Parse(json_response, QueryAccountResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self.rest_api.query(f"/cosmos/auth/v1beta1/params")
        return Parse(json_response, QueryParamsResponse())
