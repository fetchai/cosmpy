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

"""Tests for REST implementation of cfedistributor."""

import unittest

import pytest
from google.protobuf.json_format import ParseDict

from cosmpy.cfedistributor.rest_client import CfeDistributorRestClient
from cosmpy.common.utils import json_encode
from cosmpy.protos.c4echain.cfedistributor.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
    QueryStatesRequest,
    QueryStatesResponse
)
from tests.helpers import MockRestClient


class CfeDistributorRestClientTestCase(unittest.TestCase):
    """Test case for Auth module."""

    @pytest.mark.skip()
    @staticmethod
    def test_query_states():
        """Test query account for positive result."""
        content = {
                "states": [
                    {
                        "account": {
                            "id": "c4e10ep2sxpf2kj6j26w7f4uuafedkuf9sf9xqq3sl",
                            "type": "BASE_ACCOUNT"
                        },
                        "burn": False,
                        "remains": [
                            {
                                "denom": "uc4e",
                                "amount": "0.650000000000000000"
                            }
                        ]
                    }
                ],
                "coins_on_distributor_account": [
                    {
                        "denom": "uc4e",
                        "amount": "3"
                    }
                ]
            }
        expected_response = ParseDict(content, QueryStatesResponse())

        mock_client = MockRestClient(json_encode(content))
        distributor = CfeDistributorRestClient(mock_client)

        assert distributor.States(QueryStatesRequest()) == expected_response
        assert mock_client.last_base_url == "/c4e/distributor/v1beta1/states"

    @staticmethod
    def test_query_params():
        """Test query params for positive result."""
        content = {
                "params": {
                    "sub_distributors": [
                        {
                            "name": "inflation_and_fee_distributor",
                            "sources": [
                                {
                                    "id": "c4e_distributor",
                                    "type": "MAIN"
                                }
                            ],
                            "destinations": {
                                "primary_share": {
                                    "id": "validators_rewards_collector",
                                    "type": "MODULE_ACCOUNT"
                                },
                                "burn_share": "0.000000000000000000",
                                "shares": [
                                    {
                                        "name": "usage_incentives",
                                        "share": "0.300000000000000000",
                                        "destination": {
                                            "id": "usage_incentives_collector",
                                            "type": "INTERNAL_ACCOUNT"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        expected_response = ParseDict(content, QueryParamsResponse())

        mock_client = MockRestClient(json_encode(content))
        distributor = CfeDistributorRestClient(mock_client)

        assert distributor.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/c4e/distributor/v1beta1/params"
