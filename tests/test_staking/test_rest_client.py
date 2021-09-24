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
from unittest import TestCase

from google.protobuf.json_format import ParseDict

from cosmpy.protos.cosmos.staking.v1beta1.query_pb2 import (
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
from cosmpy.staking.rest_client import StakingRestClient
from tests.helpers import MockRestClient


class StakingRestClientTestCase(TestCase):
    """Test case for StakingRestClient class."""

    @staticmethod
    def test_Validators():
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

    @staticmethod
    def test_Validator():
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

    @staticmethod
    def test_ValidatorDelegations():
        """Test ValidatorDelegations method."""

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

    @staticmethod
    def test_ValidatorUnbondingDelegations():
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

    @staticmethod
    def test_Delegation():
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

    @staticmethod
    def test_UnbondingDelegation():
        """Test UnbondingDelegation method."""

        content = {
            "unbond": {
                "delegator_address": "fetchdelegator",
                "validator_address": "fetchvalidator",
                "entries": [
                    {
                        "creation_height": "1",
                        "completion_time": "2021-08-18T11:55:13.614Z",
                        "initial_balance": "123",
                        "balance": "1234",
                    }
                ],
            }
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryUnbondingDelegationResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.UnbondingDelegation(
                QueryUnbondingDelegationRequest(
                    validator_addr="validator_addr", delegator_addr="delegator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/validators/validator_addr/delegations/delegator_addr/unbonding_delegation"
        )

    @staticmethod
    def test_DelegatorDelegations():
        """Test DelegatorDelegations method."""

        content = {
            "delegation_responses": [
                {
                    "delegation": {
                        "delegator_address": "fetchdelegator",
                        "validator_address": "fetchvalidator",
                        "shares": "123",
                    },
                    "balance": {"denom": "atestfet", "amount": "123"},
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }
        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryDelegatorDelegationsResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.DelegatorDelegations(
                QueryDelegatorDelegationsRequest(delegator_addr="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/delegations/delegator_addr"
        )

    @staticmethod
    def test_DelegatorUnbondingDelegations():
        """Test DelegatorUnbondingDelegations method."""

        content = {
            "unbonding_responses": [
                {
                    "delegator_address": "fetchdelegator",
                    "validator_address": "fetchvalidator",
                    "entries": [
                        {
                            "creation_height": "123",
                            "completion_time": "2021-08-18T12:07:23.832Z",
                            "initial_balance": "123",
                            "balance": "1234",
                        }
                    ],
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(
            content, QueryDelegatorUnbondingDelegationsResponse()
        )

        staking = StakingRestClient(mock_client)

        assert (
            staking.DelegatorUnbondingDelegations(
                QueryDelegatorUnbondingDelegationsRequest(
                    delegator_addr="delegator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/delegators/delegator_addr/unbonding_delegations"
        )

    @staticmethod
    def test_Redelegations():
        """Test Redelegations method."""

        content = {
            "redelegation_responses": [
                {
                    "redelegation": {
                        "delegator_address": "fetchdelegator",
                        "validator_src_address": "fetchsrc",
                        "validator_dst_address": "fetchdst",
                        "entries": [
                            {
                                "creation_height": "123",
                                "completion_time": "2021-08-18T12:10:21.412Z",
                                "initial_balance": "123",
                                "shares_dst": "123",
                            }
                        ],
                    },
                    "entries": [
                        {
                            "redelegation_entry": {
                                "creation_height": "123",
                                "completion_time": "2021-08-18T12:10:21.412Z",
                                "initial_balance": "123",
                                "shares_dst": "123",
                            },
                            "balance": "123",
                        }
                    ],
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryRedelegationsResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.Redelegations(
                QueryRedelegationsRequest(delegator_addr="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/delegators/delegator_addr/redelegations"
        )

    @staticmethod
    def test_DelegatorValidators():
        """Test DelegatorValidators method."""

        content = {
            "validators": [
                {
                    "operator_address": "fetchoperator",
                    "jailed": True,
                    "status": "BOND_STATUS_UNSPECIFIED",
                    "tokens": "123",
                    "delegator_shares": "123",
                    "description": {
                        "moniker": "string",
                        "identity": "string",
                        "website": "string",
                        "security_contact": "string",
                        "details": "string",
                    },
                    "unbonding_height": "123",
                    "unbonding_time": "2021-08-18T12:14:55.780Z",
                    "commission": {
                        "commission_rates": {
                            "rate": "123",
                            "max_rate": "1234",
                            "max_change_rate": "1234",
                        },
                        "update_time": "2021-08-18T12:14:55.780Z",
                    },
                    "min_self_delegation": "123",
                }
            ],
            "pagination": {"next_key": "", "total": "0"},
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryDelegatorValidatorsResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.DelegatorValidators(
                QueryDelegatorValidatorsRequest(delegator_addr="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/delegators/delegator_addr/validators"
        )

    @staticmethod
    def test_DelegatorValidator():
        """Test DelegatorValidator method."""

        content = {
            "validator": {
                "operator_address": "fetchoperator",
                "jailed": True,
                "status": "BOND_STATUS_UNSPECIFIED",
                "tokens": "123",
                "delegator_shares": "123",
                "description": {
                    "moniker": "string",
                    "identity": "string",
                    "website": "string",
                    "security_contact": "string",
                    "details": "string",
                },
                "unbonding_height": "123",
                "unbonding_time": "2021-08-18T12:17:33.141Z",
                "commission": {
                    "commission_rates": {
                        "rate": "123",
                        "max_rate": "1234",
                        "max_change_rate": "1234",
                    },
                    "update_time": "2021-08-18T12:17:33.141Z",
                },
                "min_self_delegation": "123",
            }
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryDelegatorValidatorResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.DelegatorValidator(
                QueryDelegatorValidatorRequest(
                    validator_addr="validator_addr", delegator_addr="delegator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/staking/v1beta1/delegators/delegator_addr/validators/validator_addr"
        )

    @staticmethod
    def test_HistoricalInfo():
        """Test HistoricalInfo method."""

        content = {
            "hist": {
                "header": {
                    "version": {"block": "123", "app": "123"},
                    "chain_id": "string",
                    "height": "123",
                    "time": "2021-08-18T12:19:32.225Z",
                    "last_block_id": {
                        "hash": "string",
                        "part_set_header": {"total": 0, "hash": "string"},
                    },
                    "last_commit_hash": "string",
                    "data_hash": "string",
                    "validators_hash": "string",
                    "next_validators_hash": "string",
                    "consensus_hash": "string",
                    "app_hash": "string",
                    "last_results_hash": "string",
                    "evidence_hash": "string",
                    "proposer_address": "string",
                },
                "valset": [
                    {
                        "operator_address": "fetchoperator",
                        "jailed": True,
                        "status": "BOND_STATUS_UNSPECIFIED",
                        "tokens": "123",
                        "delegator_shares": "123",
                        "description": {
                            "moniker": "string",
                            "identity": "string",
                            "website": "string",
                            "security_contact": "string",
                            "details": "string",
                        },
                        "unbonding_height": "123",
                        "unbonding_time": "2021-08-18T12:19:32.225Z",
                        "commission": {
                            "commission_rates": {
                                "rate": "123",
                                "max_rate": "1234",
                                "max_change_rate": "1234",
                            },
                            "update_time": "2021-08-18T12:19:32.225Z",
                        },
                        "min_self_delegation": "123",
                    }
                ],
            }
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryHistoricalInfoResponse())

        staking = StakingRestClient(mock_client)

        assert (
            staking.HistoricalInfo(QueryHistoricalInfoRequest(height=1))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/staking/v1beta1/historical_info/1"

    @staticmethod
    def test_Pool():
        """Test Pool method."""

        content = {"pool": {"not_bonded_tokens": "123", "bonded_tokens": "123"}}

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryPoolResponse())

        staking = StakingRestClient(mock_client)

        assert staking.Pool(QueryPoolRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/staking/v1beta1/pool"

    @staticmethod
    def test_Params():
        """Test Params method."""

        content = {
            "params": {
                "unbonding_time": "123s",
                "max_validators": 0,
                "max_entries": 0,
                "historical_entries": 0,
                "bond_denom": "atestfet",
            }
        }

        mock_client = MockRestClient(json.dumps(content))

        expected_response = ParseDict(content, QueryParamsResponse())

        staking = StakingRestClient(mock_client)

        assert staking.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/staking/v1beta1/params"
