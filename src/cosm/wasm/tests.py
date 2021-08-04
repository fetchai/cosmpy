import unittest
from cosm.wasm.rest_client import WasmRestClient
from cosm.tests.helpers import MockQueryRestClient
import base64

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

    def test_query_code(self):
        content = {
            "code_info": {"code_id": 3, "creator": "fetchaddress", "data_hash": "hash"},
            "data": "bytecode",
        }
        expected_response = ParseDict(content, QueryCodeResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        wasm = WasmRestClient(mock_client)

        assert wasm.Code(QueryCodeRequest(code_id=1)) == expected_response
        assert mock_client.last_request == "/wasm/v1beta1/code/1?"

    def test_query_smart_contract_state(self):
        raw_content = b'{\n  "data": {"balance":"1"}\n}'
        expected_response = QuerySmartContractStateResponse(data=b'{"balance": "1"}')

        mock_client = MockQueryRestClient(raw_content)
        wasm = WasmRestClient(mock_client)

        assert (
            wasm.SmartContractState(
                QuerySmartContractStateRequest(
                    address="fetchcontractaddress", query_data=b"{}"
                )
            )
            == expected_response  # noqa W503
        )
        assert (
            mock_client.last_request
            == "/wasm/v1beta1/contract/fetchcontractaddress/smart/e30=?"  # noqa W503
        )

    def test_query_raw_contract_state(self):
        raw_content = b'{\n  "data": {"balance":"1"}\n}'
        expected_response = QueryRawContractStateResponse(data=b'{"balance": "1"}')

        mock_client = MockQueryRestClient(raw_content)
        wasm = WasmRestClient(mock_client)

        assert (
            wasm.RawContractState(
                QueryRawContractStateRequest(
                    address="fetchcontractaddress", query_data=b"{}"
                )
            )
            == expected_response  # noqa W503
        )
        assert (
            mock_client.last_request
            == "/wasm/v1beta1/contract/fetchcontractaddress/raw/e30=?"  # noqa W503
        )

    def test_query_all_contract_state(self):
        content = {
            "models": [
                {
                    "key": "00047572697300000000000000000000000000000000000000000000000000000000000004D2",
                    "value": "c29tZV9wYXRo",
                },
            ],
            "pagination": {"next_key": None, "total": "3"},
        }

        expected_response = ParseDict(content, QueryAllContractStateResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        wasm = WasmRestClient(mock_client)

        assert (
            wasm.AllContractState(
                QueryAllContractStateRequest(address="fetchcontractaddress")
            )
            == expected_response  # noqa W503
        )
        assert (
            mock_client.last_request
            == "/wasm/v1beta1/contract/fetchcontractaddress/state?"  # noqa W503
        )

    def test_query_contract_info(self):
        content = {
            "address": "some_address",
            "contract_info": {
                "code_id": "2",
                "creator": "other_address",
                "admin": "",
                "label": "contract",
                "ibc_port_id": "",
            },
        }

        expected_response = ParseDict(content, QueryContractInfoResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        wasm = WasmRestClient(mock_client)

        assert (
            wasm.ContractInfo(QueryContractInfoRequest(address="fetchcontractaddress"))
            == expected_response  # noqa W503
        )
        assert (
            mock_client.last_request == "/wasm/v1beta1/contract/fetchcontractaddress?"
        )

    def test_query_contract_by_code(self):
        content = {
            "contracts": ["fetch18vd8fpwxzck93qlwghaj6arh4p7c5n890l3amr"],
            "pagination": {"total": "1"},
        }

        expected_response = ParseDict(content, QueryContractsByCodeResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        wasm = WasmRestClient(mock_client)

        assert (
            wasm.ContractsByCode(QueryContractsByCodeRequest(code_id=1))
            == expected_response  # noqa W503
        )
        assert mock_client.last_request == "/wasm/v1beta1/code/1/contracts?"

    def test_query_contract_history(self):
        msg = {}
        base64_msg = base64.b64encode(json.dumps(msg).encode("UTF8")).decode()

        content = {
            "entries": [
                {
                    "operation": "CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT",
                    "code_id": "2",
                    "msg": base64_msg,
                }
            ],
            "pagination": {"total": "1"},
        }

        expected_response = ParseDict(content, QueryContractHistoryResponse())

        # Replace base64 msg with original dict which would be returned by REST api to generate get response
        content["entries"][0]["msg"] = msg
        raw_content = json.dumps(content)
        mock_client = MockQueryRestClient(raw_content)

        wasm = WasmRestClient(mock_client)

        assert (
            wasm.ContractHistory(
                QueryContractHistoryRequest(address="fetchcontractaddress")
            )
            == expected_response  # noqa W503
        )
        assert (
            mock_client.last_request
            == "/wasm/v1beta1/contract/fetchcontractaddress/history?"  # noqa W503
        )
