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

import json
from typing import List, Optional
from unittest import TestCase

from google.protobuf.descriptor import Descriptor
from google.protobuf.json_format import ParseDict

from pycosm.common.rest_client import RestClient
from pycosm.protos.cosmos.staking.v1beta1.query_pb2 import (
    QueryDelegationRequest,
    QueryDelegationResponse,
    QueryDelegatorDelegationsRequest,
    QueryDelegatorDelegationsResponse,
    QueryDelegatorUnbondingDelegationsRequest,
    QueryDelegatorUnbondingDelegationsResponse,
    QueryDelegatorValidatorRequest,
    QueryDelegatorValidatorResponse,
    QueryDelegatorValidatorsRequest,
    QueryDelegatorValidatorsResponse,
    QueryHistoricalInfoRequest,
    QueryHistoricalInfoResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryPoolRequest,
    QueryPoolResponse,
    QueryRedelegationsRequest,
    QueryRedelegationsResponse,
    QueryUnbondingDelegationRequest,
    QueryUnbondingDelegationResponse,
    QueryValidatorDelegationsRequest,
    QueryValidatorDelegationsResponse,
    QueryValidatorRequest,
    QueryValidatorResponse,
    QueryValidatorsRequest,
    QueryValidatorsResponse,
    QueryValidatorUnbondingDelegationsRequest,
    QueryValidatorUnbondingDelegationsResponse,
)
from pycosm.staking.rest_client import StakingRestClient


class MockRestClient(RestClient):
    """Mock QueryRestClient"""

    def __init__(self, content: bytes):
        """Initialize."""
        self.content: bytes = content
        self.last_base_url: Optional[str] = None
        self.last_request: Optional[Descriptor] = None
        self.last_used_params: Optional[List[str]] = None

        super().__init__("")

    def get(
        self,
        url_base_path: str,
        request: Optional[Descriptor] = None,
        used_params: Optional[List[str]] = None,
    ) -> bytes:
        """Handle GET request."""
        self.last_base_url = url_base_path
        self.last_request = request
        self.last_used_params = used_params

        return self.content

    def post(self, url_base_path: str, request: Descriptor) -> bytes:
        """Send a POST request"""
        self.last_base_url = url_base_path
        self.last_request = request

        return self.content


class StakingRestClientTestCase(TestCase):
    """Test case for StakingRestClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up test case."""
        content = {}

        mock_client = MockRestClient(json.dumps(content))
        cls.client = StakingRestClient(mock_client)

    def test_Validators(self):
        """Test Validators method."""
        content = {
            "validators": [
                {
                    "operator_address": "string",
                    "jailed": True,
                    "status": "BOND_STATUS_UNSPECIFIED",
                    "tokens": "123",
                    "delegator_shares": "string",
                    "description": {
                        "moniker": "string",
                        "identity": "string",
                        "website": "string",
                        "security_contact": "string",
                        "details": "string",
                    },
                    "unbonding_height": "1",
                    "unbonding_time": "2021-08-18T11:23:18.208Z",
                    "commission": {
                        "commission_rates": {
                            "rate": "0",
                            "max_rate": "1",
                            "max_change_rate": "1",
                        },
                        "update_time": "2021-08-18T11:23:18.208Z",
                    },
                    "min_self_delegation": "0",
                }
            ],
            "pagination": {"next_key": "", "total": "1"},
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryValidatorsResponse())

        staking = StakingRestClient(mock_client)

        assert staking.Validators(QueryValidatorsRequest() == expected_response)
        assert mock_client.last_base_url == "/cosmos/staking/v1beta1/validators"

    def test_Validator(self):
        """Test Validator method."""
        content = {
            "validator": {
                "operator_address": "string",
                "jailed": True,
                "status": "BOND_STATUS_UNSPECIFIED",
                "tokens": "string",
                "delegator_shares": "string",
                "description": {
                    "moniker": "string",
                    "identity": "string",
                    "website": "string",
                    "security_contact": "string",
                    "details": "string",
                },
                "unbonding_height": "0",
                "unbonding_time": "2021-08-18T10:33:53.339Z",
                "min_self_delegation": "string",
            }
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryValidatorResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.Validator(QueryValidatorRequest(validator_addr="validator_addr"))
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/validators/validator_addr"
        )

    def test_ValidatorDelegations(self):
        """Test ValidatorDelegations method."""
        request = QueryValidatorDelegationsRequest(validator_addr="validator_addr")
        result = self.client.ValidatorDelegations(request)
        self.assertIsInstance(result, QueryValidatorDelegationsResponse)

        content = {
            "delegation_responses": [
                {
                    "delegation": {
                        "delegator_address": "fetchdelegator",
                        "validator_address": "fetchvalidator",
                        "shares": "123",
                    },
                    "balance": {"denom": "atestfet", "amount": "12345"},
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryValidatorDelegationsResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.ValidatorDelegations(
                QueryValidatorDelegationsRequest(validator_addr="validator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/validators/validator_addr/delegations"
        )

    def test_ValidatorUnbondingDelegations(self):
        """Test ValidatorUnbondingDelegations method."""
        content = {
            "unbonding_responses": [
                {
                    "delegator_address": "fetchddelegator",
                    "validator_address": "fetchvalidator",
                    "entries": [
                        {
                            "creation_height": "123",
                            "completion_time": "2021-08-18T11:42:45.657Z",
                            "initial_balance": "12",
                            "balance": "123",
                        }
                    ],
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(
            content, QueryValidatorUnbondingDelegationsResponse()
        )

        staking = StakingRestClient(mock_client)

        assert (
            staking.ValidatorUnbondingDelegations(
                QueryValidatorUnbondingDelegationsRequest(
                    validator_addr="validator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/validators/validator_addr/unbonding_delegations"
        )

    def test_Delegation(self):
        """Test Delegation method."""

        content = {
            "delegation_response": {
                "delegation": {
                    "delegator_address": "fetchdelegator",
                    "validator_address": "fetchvalidator",
                    "shares": "123",
                },
                "balance": {"denom": "atestfet", "amount": "123"},
            }
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryDelegationResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.Delegation(
                QueryDelegationRequest(
                    validator_addr="validator_addr", delegator_addr="delegator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/validators/validator_addr/delegations/delegator_addr"
        )

    def test_UnbondingDelegation(self):
        """Test UnbondingDelegation method."""
        request = QueryUnbondingDelegationRequest(
            validator_addr="validator_addr", delegator_addr="delegator_addr"
        )
        result = self.client.UnbondingDelegation(request)
        self.assertIsInstance(result, QueryUnbondingDelegationResponse)

    def test_DelegatorDelegations(self):
        """Test DelegatorDelegations method."""
        request = QueryDelegatorDelegationsRequest(delegator_addr="delegator_addr")
        result = self.client.DelegatorDelegations(request)
        self.assertIsInstance(result, QueryDelegatorDelegationsResponse)

    def test_DelegatorUnbondingDelegations(self):
        """Test DelegatorUnbondingDelegations method."""
        request = QueryDelegatorUnbondingDelegationsRequest(
            delegator_addr="delegator_addr"
        )
        result = self.client.DelegatorUnbondingDelegations(request)
        self.assertIsInstance(result, QueryDelegatorUnbondingDelegationsResponse)

    def test_Redelegations(self):
        """Test Redelegations method."""
        request = QueryRedelegationsRequest(delegator_addr="delegator_addr")
        result = self.client.Redelegations(request)
        self.assertIsInstance(result, QueryRedelegationsResponse)

    def test_DelegatorValidators(self):
        """Test DelegatorValidators method."""
        request = QueryDelegatorValidatorsRequest(delegator_addr="delegator_addr")
        result = self.client.DelegatorValidators(request)
        self.assertIsInstance(result, QueryDelegatorValidatorsResponse)

    def test_DelegatorValidator(self):
        """Test DelegatorValidator method."""
        request = QueryDelegatorValidatorRequest(
            validator_addr="validator_addr", delegator_addr="delegator_addr"
        )
        result = self.client.DelegatorValidator(request)
        self.assertIsInstance(result, QueryDelegatorValidatorResponse)

    def test_HistoricalInfo(self):
        """Test HistoricalInfo method."""
        request = QueryHistoricalInfoRequest(height=1)
        result = self.client.HistoricalInfo(request)
        self.assertIsInstance(result, QueryHistoricalInfoResponse)

    def test_Pool(self):
        """Test Pool method."""
        request = QueryPoolRequest()
        result = self.client.Pool(request)
        self.assertIsInstance(result, QueryPoolResponse)

    def test_Params(self):
        """Test Params method."""
        request = QueryParamsRequest()
        result = self.client.Params(request)
        self.assertIsInstance(result, QueryParamsResponse)
