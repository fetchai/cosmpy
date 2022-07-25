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
"""Tests for REST implementation of Cosmos Upgrade."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import Int32Value  # noqa # needed for protobuf decode

from cosmpy.common.utils import json_encode
from cosmpy.protos.cosmos.upgrade.v1beta1.query_pb2 import (
    QueryAppliedPlanRequest,
    QueryAppliedPlanResponse,
    QueryCurrentPlanRequest,
    QueryCurrentPlanResponse,
)
from cosmpy.upgrade.rest_client import CosmosUpgradeRestClient
from tests.helpers import MockRestClient


class CosmosUpgradeRestClientTestCase(TestCase):
    """Test case for CosmosUpgradeRestClient class."""

    REST_CLIENT = CosmosUpgradeRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, CosmosUpgradeRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_CurrentPlan(self):
        """Test CurrentPlan method."""
        content = {
            "plan": {
                "name": "string",
                "time": "2022-03-29T10:02:52.926Z",
                "height": "1",
                "info": "string",
            }
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryCurrentPlanResponse())

        assert rest_client.CurrentPlan(QueryCurrentPlanRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/upgrade/v1beta1/current_plan"

    def test_AppliedPlan(self):
        """Test AppliedPlan method."""
        content = {"height": "12"}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryAppliedPlanResponse())

        assert (
            rest_client.AppliedPlan(QueryAppliedPlanRequest(name="test"))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/upgrade/v1beta1/applied_plan/test"
