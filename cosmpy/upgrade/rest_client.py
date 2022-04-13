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
from google.protobuf.json_format import Parse

from cosmpy.common.rest_client import RestClient
from cosmpy.protos.cosmos.upgrade.v1beta1.query_pb2 import (
    QueryAppliedPlanRequest,
    QueryAppliedPlanResponse,
    QueryCurrentPlanRequest,
    QueryCurrentPlanResponse,
    QueryUpgradedConsensusStateRequest,
    QueryUpgradedConsensusStateResponse,
)
from cosmpy.upgrade.interface import CosmosUpgrade


class CosmosUpgradeRestClient(CosmosUpgrade):
    """Cosmos Upgrade REST client."""

    API_URL = "/cosmos/upgrade/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def CurrentPlan(self, request: QueryCurrentPlanRequest) -> QueryCurrentPlanResponse:
        """
        CurrentPlan queries the current upgrade plan.

        :param request: QueryCurrentPlanRequest
        :return: QueryCurrentPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/current_plan",
        )
        return Parse(json_response, QueryCurrentPlanResponse())

    def AppliedPlan(self, request: QueryAppliedPlanRequest) -> QueryAppliedPlanResponse:
        """
        AppliedPlan queries a previously applied upgrade plan by its name.

        :param request: QueryAppliedPlanRequest
        :return: QueryAppliedPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/applied_plan/{request.name}", request
        )
        return Parse(json_response, QueryAppliedPlanResponse())

    def UpgradedConsensusState(
        self, request: QueryUpgradedConsensusStateRequest
    ) -> QueryUpgradedConsensusStateResponse:
        """
        UpgradedConsensusState queries the consensus state that will serve as a trusted kernel for the next version of this chain. It will only be stored at the last height of this chain.UpgradedConsensusState RPC not supported with legacy querier

        :param request: QueryUpgradedConsensusStateRequest
        :return: QueryUpgradedConsensusStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/upgraded_consensus_state/{request.last_height}", request
        )
        return Parse(json_response, QueryUpgradedConsensusStateResponse())
