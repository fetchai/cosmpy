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
from cosmpy.protos.cosmos.upgrade.v1beta1.query_pb2 import (
    QueryAppliedPlanRequest,
    QueryAppliedPlanResponse,
    QueryCurrentPlanRequest,
    QueryCurrentPlanResponse,
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

    def CurrentPlan(
        self,
        request: QueryCurrentPlanRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryCurrentPlanResponse:
        """
        CurrentPlan queries the current upgrade plan.

        :param request: QueryCurrentPlanRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryCurrentPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/current_plan",
        )
        return Parse(json_response, QueryCurrentPlanResponse())

    def AppliedPlan(
        self,
        request: QueryAppliedPlanRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryAppliedPlanResponse:
        """
        AppliedPlan queries a previously applied upgrade plan by its name.

        :param request: QueryAppliedPlanRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryAppliedPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/applied_plan/{request.name}", request
        )
        return Parse(json_response, QueryAppliedPlanResponse())
