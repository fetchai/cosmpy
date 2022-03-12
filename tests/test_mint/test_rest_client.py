# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#   Modifications copyright (C) 2022 Cros-Nest
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

"""Tests for REST implementation of Mint."""
import base64
import json
import unittest

from google.protobuf.json_format import ParseDict

from cosmpy.mint.rest_client import MintRestClient
from cosmpy.protos.cosmos.mint.v1beta1.query_pb2 import (
    QueryAnnualProvisionsResponse,
    QueryInflationResponse,
    QueryParamsResponse,
)
from tests.helpers import MockRestClient


class MintRestClientTestCase(unittest.TestCase):
    """Test case of Mint module."""

    @staticmethod
    def test_AnnualProvisions():
        """Test query annual provision for the positive result."""
        content = {"annual_provisions": base64.encode("123")}

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryAnnualProvisionsResponse())

        mint = MintRestClient(mock_client)

        assert mint.AnnualProvisions() == expected_response
        assert expected_response.annual_provision == "123"
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/annual_provisions"

    @staticmethod
    def test_Inflation():
        """Test query inflation for the positive result."""
        content = {"inflation": "string"}

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryInflationResponse())

        mint = MintRestClient(mock_client)

        assert mint.Inflation() == expected_response
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/inflation"

    @staticmethod
    def test_query_params():
        """Test query params for the positive result."""
        content = {
            "params": {
                "mint_denom": "string",
                "inflation_rate_change": "0.2",
                "inflation_max": "0.5",
                "inflation_min": "0.1",
                "goal_bonded": "0.3",
                "blocks_per_year": "1234",
            }
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryParamsResponse())

        mint = MintRestClient(mock_client)

        assert mint.Params() == expected_response
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/params"
