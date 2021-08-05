import base64
import json
from urllib.parse import urlencode

from google.protobuf.json_format import MessageToDict, Parse, ParseDict

from common import JSONLike
from cosm.query.rest_client import QueryRestClient
from cosm.wasm.interface import Wasm
from cosmwasm.wasm.v1beta1.query_pb2 import (
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
    QuerySmartContractStateRequest,
    QuerySmartContractStateResponse,
)


class WasmRestClient(Wasm):
    API_URL = "/wasm/v1beta1"

    def __init__(self, rest_api: QueryRestClient):
        """
        Create CosmWasm rest client

        :param rest_api: QueryRestClient api
        """
        self._rest_api = rest_api

    def ContractInfo(
        self, request: QueryContractInfoRequest
    ) -> QueryContractInfoResponse:
        """
        Gets the contract meta data

        :param request: QueryContractInfoRequest

        :return: QueryContractInfoResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("address")
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/contract/{request.address}?{url_encoded_request}",
        )
        return Parse(response, QueryContractInfoResponse())

    def ContractHistory(
        self, request: QueryContractHistoryRequest
    ) -> QueryContractHistoryResponse:
        """
        Gets the contract code history

        :param request: QueryContractHistoryRequest

        :return: QueryContractHistoryResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("address")
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/contract/{request.address}/history?{url_encoded_request}",
        )

        return ParseDict(
            self._fix_history_response(response), QueryContractHistoryResponse()
        )

    def ContractsByCode(
        self, request: QueryContractsByCodeRequest
    ) -> QueryContractsByCodeResponse:
        """
        Lists all smart contracts for a code id

        :param request: QueryContractsByCodeRequest

        :return: QueryContractsByCodeResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("codeId")
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/code/{request.code_id}/contracts?{url_encoded_request}",
        )
        return Parse(response, QueryContractsByCodeResponse())

    def AllContractState(
        self, request: QueryAllContractStateRequest
    ) -> QueryAllContractStateResponse:
        """
        Gets all raw store data for a single contract

        :param request: QueryAllContractStateRequest

        :return: QueryAllContractStateResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("address")
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/contract/{request.address}/state?{url_encoded_request}",
        )
        return Parse(response, QueryAllContractStateResponse())

    def RawContractState(
        self, request: QueryRawContractStateRequest
    ) -> QueryRawContractStateResponse:
        """
        Gets single key from the raw store data of a contract

        :param request: QueryRawContractStateRequest

        :return: QueryRawContractStateResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("address")
        json_request.pop("queryData")
        url_encoded_request = urlencode(json_request)
        query_data = base64.b64encode(request.query_data).decode()
        response = self._rest_api.get(
            f"{self.API_URL}/contract/{request.address}/raw/{query_data}?{url_encoded_request}",
        )

        # JSON in JSON workaround
        dict_response = json.loads(response)
        dict_response["data"] = base64.b64encode(
            json.dumps(dict_response["data"]).encode("UTF8")
        ).decode()

        return ParseDict(dict_response, QueryRawContractStateResponse())

    def SmartContractState(
        self, request: QuerySmartContractStateRequest
    ) -> QuerySmartContractStateResponse:
        """
        Get smart query result from the contract

        :param request: QuerySmartContractStateRequest

        :return: QuerySmartContractStateResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("address")
        json_request.pop("queryData")
        url_encoded_request = urlencode(json_request)
        query_data = base64.b64encode(request.query_data).decode()
        response = self._rest_api.get(
            f"{self.API_URL}/contract/{request.address}/smart/{query_data}?{url_encoded_request}",
        )

        return ParseDict(
            self._fix_state_response(response), QuerySmartContractStateResponse()
        )

    def Code(self, request: QueryCodeRequest) -> QueryCodeResponse:
        """
        Gets the binary code and metadata for a singe wasm code

        :param request: QueryCodeRequest

        :return: QueryCodeResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("codeId")
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/code/{request.code_id}?{url_encoded_request}",
        )

        return Parse(response, QueryCodeResponse())

    def Codes(self, request: QueryCodesRequest) -> QueryCodesResponse:
        """
        Gets the metadata for all stored wasm codes

        :param request: QueryCodesRequest

        :return: QueryCodesResponse
        """
        json_request = MessageToDict(request)
        url_encoded_request = urlencode(json_request)
        response = self._rest_api.get(
            f"{self.API_URL}/code?{url_encoded_request}",
        )
        return Parse(response, QueryCodesResponse())

    @staticmethod
    def _fix_state_response(response: str) -> JSONLike:
        """
        Fix raw/smart contract state response to be parsable to protobuf object
        - Converts dict to base64 encoded string

        :param response: raw/smart contract state response
        :return: Fixed response in form of dict
        """
        dict_response = json.loads(response)
        dict_response["data"] = base64.b64encode(
            json.dumps(dict_response["data"]).encode("UTF8")
        ).decode()
        return dict_response

    @staticmethod
    def _fix_history_response(response: str) -> JSONLike:
        """
        Fix contract history response to be parsable to protobuf object
        - Converts dict to base64 encoded string

        :param response: raw/smart contract state response
        :return: Fixed response in form of dict
        """
        dict_response = json.loads(response)
        for entry in dict_response["entries"]:
            entry["msg"] = base64.b64encode(
                json.dumps(entry["msg"]).encode("UTF8")
            ).decode()
        return dict_response
