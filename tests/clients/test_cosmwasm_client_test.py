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

"""Tests for the CosmWasm client module of the Clients Package."""

import json
import unittest

from google.protobuf.json_format import ParseDict

from cosmpy.clients.cosmwasm_client import CosmWasmClient
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountResponse
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceResponse
from cosmpy.protos.cosmwasm.wasm.v1beta1.query_pb2 import (
    QuerySmartContractStateResponse,
)
from tests.helpers import MockRestClient


class CosmWasmClientTests(unittest.TestCase):
    """Test case of CosmWasm client module."""

    @staticmethod
    def test_get_balance():
        """Test get balance for the positive result."""

        content = {"balance": {"denom": "stake", "amount": "1234"}}
        expected_response = ParseDict(content, QueryBalanceResponse())

        mock_rest_client = MockRestClient(json.dumps(content))
        wasm_client = CosmWasmClient(mock_rest_client)
        response = wasm_client.get_balance("account", "denom")

        assert response == expected_response
        assert (
            mock_rest_client.last_base_url
            == "/cosmos/bank/v1beta1/balances/account/denom"
        )

    @staticmethod
    def test_query_account_data():
        """Test query account data for the positive result."""

        content = {
            "account": {
                "@type": "/cosmos.auth.v1beta1.BaseAccount",
                "address": "fetch1h6974x4dspft29r9gyegtajyzaht2cdh0rt93w",
                "pub_key": {
                    "@type": "/cosmos.crypto.secp256k1.PubKey",
                    "key": "A2BjpEo54gBpulf9CrA+6tGBASFC8okaO1DYTimk/Jwp",
                },
                "account_number": "0",
                "sequence": "1",
            }
        }
        expected_response = ParseDict(content, QueryAccountResponse())

        mock_rest_client = MockRestClient(json.dumps(content))
        wasm_client = CosmWasmClient(mock_rest_client)
        response = wasm_client.query_account_data("account")

        assert response == expected_response
        assert mock_rest_client.last_base_url == "/cosmos/auth/v1beta1/accounts/address"

    @staticmethod
    def test_query_contract_state():
        """Test query contract state for the positive result."""

        raw_content = b'{\n  "data": {"balance":"1"}\n}'
        expected_response = QuerySmartContractStateResponse(data=b'{"balance": "1"}')

        mock_rest_client = MockRestClient(raw_content)
        wasm_client = CosmWasmClient(mock_rest_client)
        response = wasm_client.query_contract_state("account", "denom")

        assert response == expected_response
        assert (
            mock_rest_client.last_base_url
            == "/wasm/v1beta1/contract/fetchcontractaddress/smart/e30=?"
        )
