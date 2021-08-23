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

"""Tests for REST implementation of Auth."""

import json
import unittest

from google.protobuf.json_format import ParseDict

from cosmpy.auth.rest_client import AuthRestClient
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)
from tests.helpers import MockRestClient


class AuthTests(unittest.TestCase):
    """Test case for Auth module."""

    @staticmethod
    def test_query_account():
        """Test query account for positive result."""
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

        mock_client = MockRestClient(json.dumps(content))
        auth = AuthRestClient(mock_client)

        assert auth.Account(QueryAccountRequest(address="address")) == expected_response
        assert mock_client.last_base_url == "/cosmos/auth/v1beta1/accounts/address"

    @staticmethod
    def test_query_params():
        """Test query params for positive result."""
        content = {
            "params": {
                "max_memo_characters": 256,
                "tx_sig_limit": 7,
                "tx_size_cost_per_byte": 10,
                "sig_verify_cost_ed25519": 590,
                "sig_verify_cost_secp256k1": 1000,
            }
        }
        expected_response = ParseDict(content, QueryParamsResponse())

        mock_client = MockRestClient(json.dumps(content))
        auth = AuthRestClient(mock_client)

        assert auth.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/auth/v1beta1/params"
