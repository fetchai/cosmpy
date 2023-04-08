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

"""Interface for the cfevesting functionality of Chain4energy."""

from abc import ABC, abstractmethod

from c4epy.protos.c4echain.cfevesting.query_pb2 import (
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


class CfeVesting(ABC):
    """cfevesting abstract class."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Parameters queries the parameters of the module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """

    @abstractmethod
    def VestingType(self, request: QueryVestingTypeRequest) -> QueryVestingTypeResponse:
        """
        Query a list of VestingType items.

        :param request: QueryStatesRequest

        :return: QueryStatesResponse
        """

    @abstractmethod
    def VestingPools(
        self, request: QueryVestingPoolsRequest
    ) -> QueryVestingPoolsResponse:
        """
        Query a list of Vesting items.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """

    @abstractmethod
    def VestingsSummary(
        self, request: QueryVestingsSummaryRequest
    ) -> QueryVestingsSummaryResponse:
        """
        Query a summary of the entire vesting.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """

    @abstractmethod
    def GenesisVestingsSummary(
        self, request: QueryGenesisVestingsSummaryRequest
    ) -> QueryGenesisVestingsSummaryResponse:
        """
        Query a list of GenesisVestingsSummary items.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
