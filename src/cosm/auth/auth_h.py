from cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest, QueryAccountResponse, QueryParamsRequest, QueryParamsResponse
from cosm.auth.auth import Auth


class AuthWrapper:
    def __init__(self, auth_api: Auth):
        self.auth_api = auth_api

    def query_account(self, address: str) -> QueryAccountResponse:
        return self.auth_api.Account(QueryAccountRequest(address=address))

    def query_params(self) -> QueryParamsResponse:
        return self.auth_api.Params(QueryParamsRequest())
