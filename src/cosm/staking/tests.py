import json
from unittest import TestCase

from cosm.tests.helpers import MockQueryRestClient
from cosmos.staking.v1beta1.query_pb2 import (
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

from .rest_client import StakingRestClient


class StakingRestClientTestCase(TestCase):
    """Test case for StakingRestClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up test case."""
        cls.client = StakingRestClient("rest_address")
        content = {}

        mock_client = MockQueryRestClient(json.dumps(content))
        cls.client.rest_api = mock_client

    def test_Validators(self):
        """Test Validators method."""
        request = QueryValidatorsRequest()
        result = self.client.Validators(request)
        self.assertIsInstance(result, QueryValidatorsResponse)

    def test_Validator(self):
        """Test Validator method."""
        request = QueryValidatorRequest(validator_addr="validator_addr")
        result = self.client.Validator(request)
        self.assertIsInstance(result, QueryValidatorResponse)

    def test_ValidatorDelegations(self):
        """Test ValidatorDelegations method."""
        request = QueryValidatorDelegationsRequest(validator_addr="validator_addr")
        result = self.client.ValidatorDelegations(request)
        self.assertIsInstance(result, QueryValidatorDelegationsResponse)

    def test_ValidatorUnbondingDelegations(self):
        """Test ValidatorUnbondingDelegations method."""
        request = QueryValidatorUnbondingDelegationsRequest(
            validator_addr="validator_addr"
        )
        result = self.client.ValidatorUnbondingDelegations(request)
        self.assertIsInstance(result, QueryValidatorUnbondingDelegationsResponse)

    def test_Delegation(self):
        """Test Delegation method."""
        request = QueryDelegationRequest(
            validator_addr="validator_addr", delegator_addr="delegator_addr"
        )
        result = self.client.Delegation(request)
        self.assertIsInstance(result, QueryDelegationResponse)

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
