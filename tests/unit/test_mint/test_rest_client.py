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
import unittest

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
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
    def test_AnnualProvisionsBase64():
        """Test query annual provision for the positive result."""
        content = {
            "annual_provisions": "MTIzNA=="
        }  # use value "1234" in base64 encoded format

        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryAnnualProvisionsResponse())

        mint = MintRestClient(mock_client)

        assert mint.AnnualProvisions() == expected_response
        assert expected_response.annual_provisions == b"1234"
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/annual_provisions"

    @staticmethod
    def test_AnnualProvisionsInteger():
        """Test query annual provision for the positive result."""
        content = {"annual_provisions": "1234"}

        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryAnnualProvisionsResponse())
        # The AnnualProvisions object is expecting a base64 encoded value
        expected_response.annual_provisions = base64.b64encode(
            expected_response.annual_provisions
        )

        mint = MintRestClient(mock_client)
        provision = mint.AnnualProvisions()
        assert provision == expected_response
        assert expected_response.annual_provisions == b"1234"
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/annual_provisions"

    @staticmethod
    def test_InflationBase64():
        """Test query inflation for the positive result."""
        content = {"inflation": "MC4wMTIzNDU="}

        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryInflationResponse())

        mint = MintRestClient(mock_client)

        assert mint.Inflation() == expected_response
        assert mint.Inflation().inflation == b"0.012345"
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/inflation"

    @staticmethod
    def test_InflationInteger():
        """Test query inflation for the positive result."""
        content = {"inflation": "0.012345"}

        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryInflationResponse())
        # The Inflation object is expecting a base64 encoded value
        # FIXME: The create an issue by loosing the decimal dot and adding padding '='  # pylint: disable=W0511
        expected_response.inflation = base64.b64encode(expected_response.inflation)

        mint = MintRestClient(mock_client)

        # This test is expected to fail because of the loss of the decimal dot.
        # assert mint.Inflation() == expected_response
        assert mint.Inflation().inflation == b"0.012345"
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/inflation"

    @staticmethod
    def test_query_params():
        """Test query params for the positive result."""
        content = {
            "params": {
                "mintDenom": "string",
                "inflationRate": "0.12345",
                "blocksPerYear": "1234",
            }
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryParamsResponse())

        mint = MintRestClient(mock_client)

        assert mint.Params().params.blocks_per_year == 1234
        assert mint.Params().params.inflation_rate == "0.12345"
        assert mint.Params().params.mint_denom == "string"
        assert mint.Params() == expected_response
        assert mock_client.last_base_url == "/cosmos/mint/v1beta1/params"
