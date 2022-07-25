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
"""Tests for REST implementation of IBC Core Client."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import Int32Value  # noqa # needed for protobuf decode

from cosmpy.common.utils import json_encode
from cosmpy.ibc.core.client.rest_client import IBCCoreClientRestClient  # type: ignore
from cosmpy.protos.ibc.core.client.v1.query_pb2 import (
    QueryClientParamsRequest,
    QueryClientParamsResponse,
    QueryClientStateRequest,
    QueryClientStateResponse,
    QueryClientStatesRequest,
    QueryClientStatesResponse,
    QueryConsensusStateRequest,
    QueryConsensusStateResponse,
    QueryConsensusStatesRequest,
    QueryConsensusStatesResponse,
)
from tests.helpers import MockRestClient

TYPE = {
    "@type": "type.googleapis.com/google.protobuf.Int32Value",
    "value": "42",
}


class IBCCoreClientRestClientTestCase(TestCase):
    """Test case for IBCCoreClientRestClient class."""

    REST_CLIENT = IBCCoreClientRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, IBCCoreClientRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_ClientState(self):
        """Test ClientState method."""
        content = {
            "client_state": TYPE,
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryClientStateResponse())

        assert (
            rest_client.ClientState(QueryClientStateRequest(client_id="client_id"))
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/client/v1beta1/client_states/client_id"
        )

    def test_ClientStates(self):
        """Test ClientStates method."""
        content = {
            "client_states": [{"client_id": "string", "client_state": TYPE}],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryClientStatesResponse())

        assert rest_client.ClientStates(QueryClientStatesRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/core/client/v1beta1/client_states"

    def test_ConsensusState(self):
        """Test ConsensusState method."""
        content = {
            "consensus_state": TYPE,
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConsensusStateResponse())

        assert (
            rest_client.ConsensusState(
                QueryConsensusStateRequest(
                    revision_number=1, client_id="client_id", revision_height=1
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/client/v1beta1/consensus_states/client_id/revision/1/height/1"
        )

    def test_ConsensusStates(self):
        """Test ConsensusStates method."""
        content = {
            "consensus_states": [
                {
                    "height": {
                        "revision_number": "1",
                        "revision_height": "1",
                    },
                    "consensus_state": TYPE,
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConsensusStatesResponse())

        assert (
            rest_client.ConsensusStates(
                QueryConsensusStatesRequest(client_id="client_id")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/client/v1beta1/consensus_states/client_id"
        )

    def test_ClientParams(self):
        """Test ClientParams method."""
        content = {}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryClientParamsResponse())

        assert rest_client.ClientParams(QueryClientParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/client/v1beta1/params"
