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
from cosmpy.protos.cosmos.base.tendermint.v1beta1.query_pb2 import (
    GetBlockByHeightRequest,
    GetBlockByHeightResponse,
    GetLatestBlockRequest,
    GetLatestBlockResponse,
    GetLatestValidatorSetRequest,
    GetLatestValidatorSetResponse,
    GetNodeInfoRequest,
    GetNodeInfoResponse,
    GetSyncingRequest,
    GetSyncingResponse,
    GetValidatorSetByHeightRequest,
    GetValidatorSetByHeightResponse,
)
from cosmpy.tendermint.interface import CosmosBaseTendermint


class CosmosBaseTendermintRestClient(CosmosBaseTendermint):
    """Cosmos Base Tendermint REST client."""

    API_URL = "/cosmos/base/tendermint/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def GetNodeInfo(
        self,
        request: GetNodeInfoRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetNodeInfoResponse:
        """
        GetNodeInfo queries the current node info.

        :param request: GetNodeInfoRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetNodeInfoResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/node_info",
        )
        return Parse(json_response, GetNodeInfoResponse())

    def GetSyncing(
        self,
        request: GetSyncingRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetSyncingResponse:
        """
        GetSyncing queries node syncing.

        :param request: GetSyncingRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetSyncingResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/syncing",
        )
        return Parse(json_response, GetSyncingResponse())

    def GetLatestBlock(
        self,
        request: GetLatestBlockRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetLatestBlockResponse:
        """
        GetLatestBlock returns the latest block.

        :param request: GetLatestBlockRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetLatestBlockResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/blocks/latest",
        )
        return Parse(json_response, GetLatestBlockResponse())

    def GetBlockByHeight(
        self,
        request: GetBlockByHeightRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetBlockByHeightResponse:
        """
        GetBlockByHeight queries block for given height.

        :param request: GetBlockByHeightRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetBlockByHeightResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/blocks/{request.height}")
        return Parse(json_response, GetBlockByHeightResponse())

    def GetLatestValidatorSet(
        self,
        request: GetLatestValidatorSetRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetLatestValidatorSetResponse:
        """
        GetLatestValidatorSet queries latest validator-set.

        :param request: GetLatestValidatorSetRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetLatestValidatorSetResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validatorsets/latest", request
        )
        return Parse(json_response, GetLatestValidatorSetResponse())

    def GetValidatorSetByHeight(
        self,
        request: GetValidatorSetByHeightRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> GetValidatorSetByHeightResponse:
        """
        GetValidatorSetByHeight queries validator-set at a given height.

        :param request: GetValidatorSetByHeightRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: GetValidatorSetByHeightResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validatorsets/{request.height}", request
        )
        return Parse(json_response, GetValidatorSetByHeightResponse())
