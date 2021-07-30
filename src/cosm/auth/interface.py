from abc import ABC, abstractmethod

from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)


class Auth(ABC):
    @abstractmethod
    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        """
        Queries account data - sequence, account_id, etc.

        :param request: QueryAccountRequest that contains account address

        :return: QueryAccountResponse
        """
        pass

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Queries all parameters

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        pass
