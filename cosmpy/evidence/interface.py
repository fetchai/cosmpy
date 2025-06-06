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
"""Interface for the Evidence functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from cosmpy.protos.cosmos.evidence.v1beta1.query_pb2 import (
    QueryAllEvidenceRequest,
    QueryAllEvidenceResponse,
    QueryEvidenceRequest,
    QueryEvidenceResponse,
)


class Evidence(ABC):
    """Evidence abstract class."""

    @abstractmethod
    def Evidence(
        self,
        request: QueryEvidenceRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryEvidenceResponse:
        """
        Evidence queries evidence based on evidence hash.

        :param request: QueryEvidenceRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryEvidenceResponse
        """

    @abstractmethod
    def AllEvidence(
        self,
        request: QueryAllEvidenceRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryAllEvidenceResponse:
        """
        AllEvidence queries all evidence.

        :param request: QueryAllEvidenceRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryAllEvidenceResponse
        """
