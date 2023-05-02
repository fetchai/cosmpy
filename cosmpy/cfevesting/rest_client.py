# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022-2023 Cros Nest B.V. Limited
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

"""Implementation of cfedistributor interface using REST."""

from google.protobuf.json_format import Parse

from cosmpy.cfevesting.interface import CfeVesting
from cosmpy.common.rest_client import RestClient
from cosmpy.protos.c4echain.cfevesting.query_pb2 import (
    QueryGenesisVestingsSummaryRequest,
    QueryGenesisVestingsSummaryResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryVestingPoolsRequest,
    QueryVestingPoolsResponse,
    QueryVestingTypeRequest,
    QueryVestingTypeResponse,
    QueryVestingsSummaryRequest,
    QueryVestingsSummaryResponse,
)


class CfeVestingRestClient(CfeVesting):
    """cfevesting REST client."""

    API_URL = "/c4e/vesting/v1beta1"

    def __init__(self, rest_api: RestClient):
        """
        Initialize minter rest client.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Parameters queries the parameters of the module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())

    def VestingType(self, request: QueryVestingTypeRequest) -> QueryVestingTypeResponse:
        """
        Query a list of VestingType items.

        :param request: QueryStatesRequest

        :return: QueryStatesResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/vesting_type")
        return Parse(json_response, QueryVestingTypeResponse())

    def VestingPools(
        self, request: QueryVestingPoolsRequest
    ) -> QueryVestingPoolsResponse:
        """
        Query a list of Vesting items.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/vesting_pools/{request.owner}"
        )
        return Parse(json_response, QueryVestingPoolsResponse())

    def VestingsSummary(
        self, request: QueryVestingsSummaryRequest
    ) -> QueryVestingsSummaryResponse:
        """
        Query a summary of the entire vesting.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/summary")
        return Parse(json_response, QueryVestingsSummaryResponse())

    def GenesisVestingsSummary(
        self, request: QueryGenesisVestingsSummaryRequest
    ) -> QueryGenesisVestingsSummaryResponse:
        """
        Query a list of GenesisVestingsSummary items.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/genesis_summary")
        return Parse(json_response, QueryGenesisVestingsSummaryResponse())
