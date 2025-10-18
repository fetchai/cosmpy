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
from cosmpy.ibc.core.client.interface import IBCCoreClient  # type: ignore
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


class IBCCoreClientRestClient(IBCCoreClient):
    """IBC Core Client REST client."""

    API_URL = "/ibc/core/client/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def ClientState(
        self,
        request: QueryClientStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryClientStateResponse:
        """
        ClientState queries an IBC light client.

        :param request: QueryClientStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryClientStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/client_states/{request.client_id}"
        )
        return Parse(json_response, QueryClientStateResponse())

    def ClientStates(
        self,
        request: QueryClientStatesRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryClientStatesResponse:
        """
        ClientStates queries all the IBC light clients of a chain.

        :param request: QueryClientStatesRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryClientStatesResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/client_states", request)
        return Parse(json_response, QueryClientStatesResponse())

    def ConsensusState(
        self,
        request: QueryConsensusStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConsensusStateResponse:
        """
        ConsensusState queries a consensus state associated with a client state at a given height.

        :param request: QueryConsensusStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConsensusStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/consensus_states/{request.client_id}/revision/{request.revision_number}/height/{request.revision_height}"
        )
        return Parse(json_response, QueryConsensusStateResponse())

    def ConsensusStates(
        self,
        request: QueryConsensusStatesRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConsensusStatesResponse:
        """
        ConsensusStates queries all the consensus states associated with a given client.

        :param request: QueryConsensusStatesRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConsensusStatesResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/consensus_states/{request.client_id}", request
        )
        return Parse(json_response, QueryConsensusStatesResponse())

    def ClientParams(
        self,
        request: QueryClientParamsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryClientParamsResponse:
        """
        ClientParams queries all parameters of the IBC client.

        :param request: QueryClientParamsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryClientParamsResponse
        """
        json_response = self._rest_api.get("/ibc/client/v1beta1/params")
        return Parse(json_response, QueryClientParamsResponse())
