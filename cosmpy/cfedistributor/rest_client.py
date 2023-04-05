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

"""Implementation of cfedistributor interface using REST."""

from google.protobuf.json_format import Parse

from cosmpy.cfedistributor.interface import CfeDistributor
from cosmpy.common.rest_client import RestClient
from cosmpy.protos.c4echain.cfedistributor.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
    QueryStatesRequest,
    QueryStatesResponse
)


class CfeDistributorRestClient(CfeDistributor):
    """cfedistributor REST client."""

    API_URL = "/c4e/distributor/v1beta1"

    def __init__(self, rest_api: RestClient):
        """
        Initialize authentication rest client.

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

    def States(self, request: QueryStatesRequest) -> QueryStatesResponse:
        """
        Queries a list of States items.

        :param request: QueryStatesRequest

        :return: QueryStatesResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/states")
        return Parse(json_response, QueryStatesResponse())
