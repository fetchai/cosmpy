from google.protobuf.json_format import Parse  # noqa
import cosmos.crypto.secp256k1.keys_pb2  # noqa
from cosm.query.rest_client import QueryRestClient

from cosmwasm.wasm.v1beta1.query_pb2 import (
    QuerySmartContractStateRequest,
    QuerySmartContractStateResponse,
    QueryAllContractStateRequest,
    QueryAllContractStateResponse,
    QueryCodeRequest,
    QueryCodeResponse,
    QueryCodesRequest,
    QueryCodesResponse,
    QueryContractHistoryRequest,
    QueryContractHistoryResponse,
    QueryContractInfoRequest,
    QueryContractInfoResponse,
    QueryContractsByCodeRequest,
    QueryContractsByCodeResponse,
    QueryRawContractStateRequest,
    QueryRawContractStateResponse,
)

from cosm.auth.interface import Auth


class WasmRestClient:
    API_URL = "/cosmos/auth/v1beta1"

    def __init__(self, rest_api: QueryRestClient):
        """
        Create cosmwasm rest client

        :param rest_api: QueryRestClient apiauth
        """
        self._rest_api = rest_api

    def SmartContractState(
        self, request: QuerySmartContractStateRequest
    ) -> QuerySmartContractStateResponse:
        raise RuntimeError("TODO")

    def AllContractState(
        self, request: QueryAllContractStateRequest
    ) -> QueryAllContractStateResponse:
        raise RuntimeError("TODO")

    def Code(self, request: QueryCodeRequest) -> QueryCodeResponse:
        raise RuntimeError("TODO")

    def Codes(self, request: QueryCodesRequest) -> QueryCodesResponse:
        raise RuntimeError("TODO")

    def ContractHistory(
        self, request: QueryContractHistoryRequest
    ) -> QueryContractHistoryResponse:
        raise RuntimeError("TODO")

    def ContractInfo(
        self, request: QueryContractInfoRequest
    ) -> QueryContractInfoResponse:
        raise RuntimeError("TODO")

    def ContractsByCode(
        self, request: QueryContractsByCodeRequest
    ) -> QueryContractsByCodeResponse:
        raise RuntimeError("TODO")

    def RawContractState(
        self, request: QueryRawContractStateRequest
    ) -> QueryRawContractStateResponse:
        raise RuntimeError("TODO")
