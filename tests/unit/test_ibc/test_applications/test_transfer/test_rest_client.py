# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
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
"""Tests for REST implementation of IBC Applications Transfer."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
from cosmpy.ibc.applications.transfer.rest_client import (  # type: ignore
    IBCApplicationsTransferRestClient,
)
from cosmpy.protos.ibc.applications.transfer.v1.query_pb2 import (
    QueryDenomHashRequest,
    QueryDenomHashResponse,
    QueryDenomRequest,
    QueryDenomResponse,
    QueryDenomsRequest,
    QueryDenomsResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)

from tests.helpers import MockRestClient


class IBCApplicationsTransferRestClientTestCase(TestCase):
    """Test case for IBCApplicationsTransferRestClient class."""

    REST_CLIENT = IBCApplicationsTransferRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, IBCApplicationsTransferRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_Denom(self):
        """Test Denom method."""
        # shape according to QueryDenomResponse { denom: Denom }
        content = {
            "denom": {
                "trace": [
                    {
                        "portId": "transfer",
                        "channelId": "channel-0",
                    }
                ],
                "base": "uatom",
            }
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryDenomResponse())

        assert rest_client.Denom(QueryDenomRequest(hash="hash")) == expected_response
        assert mock_client.last_base_url == "/ibc/apps/transfer/v1/denoms/hash"

    def test_Denoms(self):
        """Test Denoms method."""
        # shape according to QueryDenomsResponse { denoms: [Denom], pagination: PageResponse }
        content = {
            "denoms": [
                {
                    "trace": [
                        {
                            "portId": "transfer",
                            "channelId": "channel-0",
                        }
                    ],
                    "base": "uatom",  # <-- 'base' here too
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryDenomsResponse())

        assert rest_client.Denoms(QueryDenomsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/apps/transfer/v1/denoms"

    def test_Params(self):
        """Test Params method."""
        # empty params is fine for a unit test; ParseDict will fill defaults
        content = {}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryParamsResponse())

        assert rest_client.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/apps/transfer/v1/params"

    def test_DenomHash(self):
        """Test DenomHash method."""
        content = {"hash": "ABCD1234"}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryDenomHashResponse())

        assert (
            rest_client.DenomHash(
                QueryDenomHashRequest(trace="transfer/channel-0/uatom")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/apps/transfer/v1/denom_hashes/transfer/channel-0/uatom"
        )
