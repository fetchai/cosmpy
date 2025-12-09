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
"""Implementation of IBC Applications Transfer  interface using REST."""
from typing import Optional, Tuple

from google.protobuf.json_format import Parse

from cosmpy.common.rest_client import RestClient
from cosmpy.ibc.core.connection.interface import IBCCoreConnection  # type: ignore
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


class IBCCoreConnectionRestClient(IBCCoreConnection):
    """IBC Core Connection REST client."""

    API_URL = "/ibc/core/connection/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Connection(
        self,
        request: QueryConnectionRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConnectionResponse:
        """
        Connection queries an IBC connection end.

        :param request: QueryConnectionRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConnectionResponse
        """  # noqa: D401
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}"
        )
        return Parse(json_response, QueryConnectionResponse())

    def Connections(
        self,
        request: QueryConnectionsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConnectionsResponse:
        """
        Connections queries all the IBC connections of a chain.

        :param request: QueryConnectionsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConnectionsResponse
        """  # noqa: D401
        json_response = self._rest_api.get(f"{self.API_URL}/connections", request)
        return Parse(json_response, QueryConnectionsResponse())

    def ClientConnections(
        self,
        request: QueryClientConnectionsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryClientConnectionsResponse:
        """
        ClientConnections queries the connection paths associated with a client state.

        :param request: QueryClientConnectionsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryClientConnectionsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/client_connections/{request.client_id}"
        )
        return Parse(json_response, QueryClientConnectionsResponse())

    def ConnectionClientState(
        self,
        request: QueryConnectionClientStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConnectionClientStateResponse:
        """
        ConnectionClientState queries the client state associated with the connection.

        :param request: QueryConnectionClientStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConnectionClientStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}/client_state"
        )
        return Parse(json_response, QueryConnectionClientStateResponse())

    def ConnectionConsensusState(
        self,
        request: QueryConnectionConsensusStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConnectionConsensusStateResponse:
        """
        ConnectionConsensusState queries the consensus state associated with the connection.

        :param request: QueryConnectionConsensusStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConnectionConsensusStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}/consensus_state/revision/{request.revision_number}/height/{request.revision_height}"
        )
        return Parse(json_response, QueryConnectionConsensusStateResponse())
