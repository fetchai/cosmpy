import unittest
from cosm.wasm.rest_client import WasmRestClient
from cosm.tests.helpers import MockQueryRestClient

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
from google.protobuf.json_format import ParseDict

import json


class WasmTests(unittest.TestCase):
    def test_query_codes(self):
        content = {
            "code_infos": [
                {"code_id": 3, "creator": "fetchaddress", "data_hash": "hash"},
            ],
            "pagination": {"total": 1},
        }
        expected_response = ParseDict(content, QueryCodesResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        wasm = WasmRestClient(mock_client)

        assert wasm.Codes(QueryCodesRequest()) == expected_response
        assert mock_client.last_request == "/wasm/v1beta1/code?"
