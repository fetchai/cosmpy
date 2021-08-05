"""Implementation of Auth interface using REST."""

from google.protobuf.json_format import Parse

from cosm.auth.interface import Auth
from cosm.common.rest_client import RestClient
from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)


class AuthRestClient(Auth):
    """Auth REST client."""

    API_URL = "/cosmos/auth/v1beta1"

    def __init__(self, rest_api: RestClient):
        """
        Initialize authentication rest client.

        :param rest_api: RestClient api
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
