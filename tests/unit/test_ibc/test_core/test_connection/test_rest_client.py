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
"""Tests for REST implementation of IBC Core Connection."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import Int32Value  # noqa # needed for protobuf decode

from cosmpy.common.utils import json_encode
from cosmpy.ibc.core.connection.rest_client import (  # type: ignore
    IBCCoreConnectionRestClient,
)
from cosmpy.protos.ibc.core.connection.v1.query_pb2 import (
    QueryClientConnectionsRequest,
    QueryClientConnectionsResponse,
    QueryConnectionClientStateRequest,
    QueryConnectionClientStateResponse,
    QueryConnectionConsensusStateRequest,
    QueryConnectionConsensusStateResponse,
    QueryConnectionRequest,
    QueryConnectionResponse,
    QueryConnectionsRequest,
    QueryConnectionsResponse,
)
from tests.helpers import MockRestClient

TYPE = {
    "@type": "type.googleapis.com/google.protobuf.Int32Value",
    "value": "42",
}


class IBCCoreConnectionRestClientTestCase(TestCase):
    """Test case for IBCCoreConnectionRestClient class."""

    REST_CLIENT = IBCCoreConnectionRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, IBCCoreConnectionRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_Connection(self):
        """Test Connection method."""
        content = {
            "connection": {
                "client_id": "string",
                "versions": [{"identifier": "string", "features": ["string"]}],
                "state": "STATE_UNINITIALIZED_UNSPECIFIED",
                "counterparty": {
                    "client_id": "1",
                    "connection_id": "1",
                    "prefix": {"key_prefix": "string"},
                },
                "delay_period": "1",
            },
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConnectionResponse())

        assert (
            rest_client.Connection(
                QueryConnectionRequest(connection_id="connection_id")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/connection/v1beta1/connections/connection_id"
        )

    def test_Connections(self):
        """Test Connections method."""
        content = {
            "connections": [
                {
                    "id": "1",
                    "client_id": "1",
                    "versions": [{"identifier": "string", "features": ["string"]}],
                    "state": "STATE_UNINITIALIZED_UNSPECIFIED",
                    "counterparty": {
                        "client_id": "1",
                        "connection_id": "1",
                        "prefix": {"key_prefix": "string"},
                    },
                    "delay_period": "1",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConnectionsResponse())

        assert rest_client.Connections(QueryConnectionsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/core/connection/v1beta1/connections"

    def test_ClientConnections(self):
        """Test ClientConnections method."""
        content = {
            "connection_paths": ["string"],
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryClientConnectionsResponse())

        assert (
            rest_client.ClientConnections(
                QueryClientConnectionsRequest(client_id="111")
            )
            == expected_response
        )
        assert [mock_client.last_base_url] == [
            "/ibc/core/connection/v1beta1/client_connections/111"
        ]

    def test_ConnectionClientState(self):
        """Test ConnectionClientState method."""
        content = {
            "identified_client_state": {
                "client_id": "string",
                "client_state": TYPE,
            },
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConnectionClientStateResponse())

        assert (
            rest_client.ConnectionClientState(
                QueryConnectionClientStateRequest(connection_id="connection_id")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/connection/v1beta1/connections/connection_id/client_state"
        )

    def test_ConnectionConsensusState(self):
        """Test ConnectionConsensusState method."""
        content = {
            "consensus_state": TYPE,
            "client_id": "string",
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConnectionConsensusStateResponse())

        assert (
            rest_client.ConnectionConsensusState(
                QueryConnectionConsensusStateRequest(
                    revision_height=1,
                    revision_number=1,
                    connection_id="connection_id",
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/connection/v1beta1/connections/connection_id/consensus_state/revision/1/height/1"
        )
