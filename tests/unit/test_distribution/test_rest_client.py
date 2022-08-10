# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#   Modifications copyright (C) 2022 Cros-Nest
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

"""Tests for REST implementation of Distribution."""

from unittest import TestCase

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
from cosmpy.distribution.rest_client import DistributionRestClient
from cosmpy.protos.cosmos.distribution.v1beta1.query_pb2 import (
    QueryCommunityPoolResponse,
    QueryDelegationRewardsRequest,
    QueryDelegationRewardsResponse,
    QueryDelegationTotalRewardsRequest,
    QueryDelegationTotalRewardsResponse,
    QueryDelegatorValidatorsRequest,
    QueryDelegatorValidatorsResponse,
    QueryDelegatorWithdrawAddressRequest,
    QueryDelegatorWithdrawAddressResponse,
    QueryParamsResponse,
    QueryValidatorCommissionRequest,
    QueryValidatorCommissionResponse,
    QueryValidatorOutstandingRewardsRequest,
    QueryValidatorOutstandingRewardsResponse,
    QueryValidatorSlashesRequest,
    QueryValidatorSlashesResponse,
)
from tests.helpers import MockRestClient


class DistributionRestClientTestCase(TestCase):
    """Test case for DistributionRestClient class."""

    @staticmethod
    def test_CommunityPool():
        """Test CommunityPool method."""
        content = {"pool": [{"denom": "string", "amount": "123"}]}
        mock_client = MockRestClient(json_encode(content).encode("utf8"))

        expected_response = ParseDict(content, QueryCommunityPoolResponse())

        distribution = DistributionRestClient(mock_client)

        assert distribution.CommunityPool() == expected_response
        assert (
            mock_client.last_base_url == "/cosmos/distribution/v1beta1/community_pool"
        )

    @staticmethod
    def test_DelegationTotalRewards():
        """Test DelegationTotalRewards method."""
        content = {
            "rewards": [
                {
                    "validator_address": "string",
                    "reward": [{"denom": "string", "amount": "123"}],
                }
            ],
            "total": [{"denom": "string", "amount": "123"}],
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryDelegationTotalRewardsResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.DelegationTotalRewards(
                QueryDelegationTotalRewardsRequest(delegator_address="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/delegators/delegator_addr/rewards"
        )

    @staticmethod
    def test_DelegationRewards():
        """Test DelegationRewards method."""
        content = {"rewards": [{"denom": "string", "amount": "1234"}]}
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryDelegationRewardsResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.DelegationRewards(
                QueryDelegationRewardsRequest(
                    delegator_address="delegator_addr",
                    validator_address="validator_addr",
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/delegators/delegator_addr/rewards/validator_addr"
        )

    @staticmethod
    def test_DelegatorValidators():
        """Test DelegatorValidators method."""
        content = {"validators": ["string"]}
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryDelegatorValidatorsResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.DelegatorValidators(
                QueryDelegatorValidatorsRequest(delegator_address="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/delegators/delegator_addr/validators"
        )

    @staticmethod
    def test_DelegatorWithdrawAddress():
        """Test DelegatorWithdrawAddress method."""
        content = {"withdraw_address": "string"}
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryDelegatorWithdrawAddressResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.DelegatorWithdrawAddress(
                QueryDelegatorWithdrawAddressRequest(delegator_address="delegator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/delegators/delegator_addr/withdraw_address"
        )

    @staticmethod
    def test_Params():
        """Test Params method."""
        content = {
            "params": {
                "community_tax": "0.1",
                "base_proposer_reward": "0.2",
                "bonus_proposer_reward": "0.3",
                "withdraw_addr_enabled": True,
            }
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryParamsResponse())

        distribution = DistributionRestClient(mock_client)

        # Check that the parameters are in the right format
        assert expected_response.params.community_tax == "0.1"
        assert expected_response.params.base_proposer_reward == "0.2"
        assert expected_response.params.bonus_proposer_reward == "0.3"
        assert expected_response.params.withdraw_addr_enabled is True

        assert distribution.Params() == expected_response
        assert mock_client.last_base_url == "/cosmos/distribution/v1beta1/params"

    @staticmethod
    def test_ValidatorCommission():
        """Test ValidatorCommission method."""
        content = {
            "commission": {"commission": [{"denom": "string", "amount": "1234"}]}
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryValidatorCommissionResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.ValidatorCommission(
                QueryValidatorCommissionRequest(validator_address="validator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/validators/validator_addr/commission"
        )

    @staticmethod
    def test_ValidatorOutstandingRewards():
        """Test ValidatorOutstandingRewards method."""
        content = {"rewards": {"rewards": [{"denom": "string", "amount": "1234"}]}}
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(
            content, QueryValidatorOutstandingRewardsResponse()
        )

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.ValidatorOutstandingRewards(
                QueryValidatorOutstandingRewardsRequest(
                    validator_address="validator_addr"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/validators/validator_addr/outstanding_rewards"
        )

    @staticmethod
    def test_ValidatorSlashes():
        """Test ValidatorSlashes method."""
        content = {
            "slashes": [{"validator_period": "1", "fraction": "1"}],
            "pagination": {"next_key": None, "total": "1"},
        }
        mock_client = MockRestClient(json_encode(content))

        expected_response = ParseDict(content, QueryValidatorSlashesResponse())

        distribution = DistributionRestClient(mock_client)

        assert (
            distribution.ValidatorSlashes(
                QueryValidatorSlashesRequest(validator_address="validator_addr")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/distribution/v1beta1/validators/validator_addr/slashes"
        )
