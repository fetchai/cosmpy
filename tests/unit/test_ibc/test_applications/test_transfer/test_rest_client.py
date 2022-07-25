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
    QueryDenomTraceRequest,
    QueryDenomTraceResponse,
    QueryDenomTracesRequest,
    QueryDenomTracesResponse,
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

    def test_DenomTrace(self):
        """Test DenomTrace method."""
        content = {"denom_trace": {"path": "string", "base_denom": "string"}}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryDenomTraceResponse())

        assert (
            rest_client.DenomTrace(QueryDenomTraceRequest(hash="hash"))
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/applications/transfer/v1beta1/denom_traces/hash"
        )

    def test_DenomTraces(self):
        """Test DenomTraces method."""
        content = {
            "denom_traces": [{"path": "string", "base_denom": "string"}],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryDenomTracesResponse())

        assert rest_client.DenomTraces(QueryDenomTracesRequest()) == expected_response
        assert (
            mock_client.last_base_url
            == "/ibc/applications/transfer/v1beta1/denom_traces"
        )

    def test_Params(self):
        """Test Params method."""
        content = {}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryParamsResponse())

        assert rest_client.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/applications/transfer/v1beta1/params"
