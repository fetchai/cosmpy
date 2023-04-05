# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
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

"""Interface for the cfeminter functionality of Chain4energy."""

from abc import ABC, abstractmethod

from cosmpy.protos.c4echain.cfeminter.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
    QueryInflationRequest,
    QueryInflationResponse,
    QueryStateRequest,
    QueryStateResponse
)


class CfeMinter(ABC):
    """cfedistributor abstract class."""
    @abstractmethod
    def Inflation(self, request: QueryInflationRequest) -> QueryInflationResponse:
        """
        Queries a list of Inflation items.

        :param request: QueryInflationRequest

        :return: QueryInflationResponse
        """
    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Parameters queries the parameters of the module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
    @abstractmethod
    def State(self, request: QueryStateRequest) -> QueryStateResponse:
        """
        Queries a list of State items.

        :param request: QueryStatesRequest

        :return: QueryStatesResponse
        """