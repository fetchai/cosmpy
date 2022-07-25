# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Tests for REST implementation of Wasm."""

import base64
import unittest

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import (
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
from tests.helpers import MockRestClient


class WasmRestClientTestCase(unittest.TestCase):
    """Test case for Wasm module."""

    @staticmethod
    def test_query_codes():
        """Test query codes for positive result."""

        content = {
            "code_infos": [
                {"code_id": 3, "creator": "fetchaddress", "data_hash": "hash"},
            ],
            "pagination": {"total": 1},
        }
        expected_response = ParseDict(content, QueryCodesResponse())

        mock_client = MockRestClient(json_encode(content))
        wasm = CosmWasmRestClient(mock_client)

        assert wasm.Codes(QueryCodesRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmwasm/wasm/v1/code"

    @staticmethod
    def test_query_code():
        """Test query code for positive result."""

        content = {
            "code_info": {"code_id": 3, "creator": "fetchaddress", "data_hash": "hash"},
            "data": "bytecode",
        }
        expected_response = ParseDict(content, QueryCodeResponse())

        mock_client = MockRestClient(json_encode(content))
        wasm = CosmWasmRestClient(mock_client)

        assert wasm.Code(QueryCodeRequest(code_id=1)) == expected_response
        assert mock_client.last_base_url == "/cosmwasm/wasm/v1/code/1"

    @staticmethod
    def test_query_smart_contract_state():
        """Test query smart contract state for positive result."""

        raw_content = b'{\n  "data": {"balance":"1"}\n}'
        expected_response = QuerySmartContractStateResponse(data=b'{"balance": "1"}')

        mock_client = MockRestClient(raw_content)
        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.SmartContractState(
                QuerySmartContractStateRequest(
                    address="fetchcontractaddress", query_data=b"{}"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmwasm/wasm/v1/contract/fetchcontractaddress/smart/e30="
        )

    @staticmethod
    def test_query_raw_contract_state():
        """Test query raw contract state for positive result."""

        raw_content = b'{\n  "data": {"balance":"1"}\n}'
        expected_response = QueryRawContractStateResponse(data=b'{"balance": "1"}')

        mock_client = MockRestClient(raw_content)
        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.RawContractState(
                QueryRawContractStateRequest(
                    address="fetchcontractaddress", query_data=b"{}"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmwasm/wasm/v1/contract/fetchcontractaddress/raw/e30="
        )

    @staticmethod
    def test_query_all_contract_state():
        """Test query all contract state for positive result."""

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

        mock_client = MockRestClient(json_encode(content))
        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.AllContractState(
                QueryAllContractStateRequest(address="fetchcontractaddress")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmwasm/wasm/v1/contract/fetchcontractaddress/state"
        )

    @staticmethod
    def test_query_contract_info():
        """Test query contract info for positive result."""

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

        mock_client = MockRestClient(json_encode(content))
        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.ContractInfo(QueryContractInfoRequest(address="fetchcontractaddress"))
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmwasm/wasm/v1/contract/fetchcontractaddress"
        )

    @staticmethod
    def test_query_contract_by_code():
        """Test query contract by code for positive result."""

        content = {
            "contracts": ["fetch18vd8fpwxzck93qlwghaj6arh4p7c5n890l3amr"],
            "pagination": {"total": "1"},
        }

        expected_response = ParseDict(content, QueryContractsByCodeResponse())

        mock_client = MockRestClient(json_encode(content))
        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.ContractsByCode(QueryContractsByCodeRequest(code_id=1))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmwasm/wasm/v1/code/1/contracts"

    @staticmethod
    def test_query_contract_history():
        """Test query contract history for positive result."""

        msg = {}
        base64_msg = base64.b64encode(json_encode(msg).encode("UTF8")).decode()

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
        raw_content = json_encode(content)
        mock_client = MockRestClient(raw_content)

        wasm = CosmWasmRestClient(mock_client)

        assert (
            wasm.ContractHistory(
                QueryContractHistoryRequest(address="fetchcontractaddress")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmwasm/wasm/v1/contract/fetchcontractaddress/history"
        )
