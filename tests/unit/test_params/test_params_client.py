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

"""Tests for REST implementation of Staking."""

from unittest import TestCase

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
from cosmpy.params.rest_client import ParamsRestClient
from cosmpy.protos.cosmos.params.v1beta1.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
)
from tests.helpers import MockRestClient


class ParamsRestClientTestCase(TestCase):
    """Test case for ParamsRestClient class."""

    @staticmethod
    def test_Validators():
        """Test Validators method."""
        content = {
            "param": {
                "subspace": "baseapp",
                "key": "BlockParams",
                "value": '{"max_bytes":"200000","max_gas":"2000000"}',
            },
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryParamsResponse())

        params = ParamsRestClient(mock_client)

        assert (
            params.Params(QueryParamsRequest(subspace="baseapp", key="BlockParams"))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/params/v1beta1/params"
