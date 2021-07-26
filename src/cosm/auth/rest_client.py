from google.protobuf.json_format import Parse
import cosmos.crypto.secp256k1.keys_pb2  # noqa
from cosm.query.rest_client import QueryRestClient

from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)
from cosm.auth.interface import Auth


class AuthRestClient(Auth):
    API_URL = "/cosmos/auth/v1beta1"

    def __init__(self, rest_api: QueryRestClient):
        """
        Create authentication rest client
        :param rest_api: QueryRestClient api
        """
        self._rest_api = rest_api

    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        """
        Queries account data - sequence, account_id, etc.
        :param request: QueryAccountRequest that contains account address
        :return: QueryAccountResponse
        """
        json_response = self._rest_api.get(
            self.API_URL + f"/accounts/{request.address}"
        )
        return Parse(json_response, QueryAccountResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Queries all parameters
        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(self.API_URL + "/params")
        return Parse(json_response, QueryParamsResponse())
