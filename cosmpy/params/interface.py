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

"""Interface for the Params functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from cosmpy.protos.cosmos.params.v1beta1.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
)


class Params(ABC):
    """Params abstract class."""

    @abstractmethod
    def Params(
        self,
        request: QueryParamsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryParamsResponse:
        """
        Params queries a specific Cosmos SDK parameter.

        :param request: QueryParamsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryParamsResponse
        """
