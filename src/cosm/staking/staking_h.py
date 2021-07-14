from cosm.query.rest_client import RestClient
from cosm.staking.staking import Staking

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
from google.protobuf.json_format import Parse


class StakingWrapper:
    """Staking module that wrapps REST queries."""

    def __init__(self, api: Staking):
        """Initialize."""
        self.api = api

    def query_validators(self) -> QueryValidatorsResponse:
        """Query Validators."""
        return self.api.Validators(QueryValidatorsRequest())

    def query_validator(self, validator_addr: str) -> QueryValidatorResponse:
        """Query Validator."""
        return self.api.Validator(QueryValidatorRequest(validator_addr=validator_addr))

    def query_validator_delegations(
        self, validator_addr: str
    ) -> QueryValidatorDelegationsResponse:
        """Query ValidatorDelegations."""
        return self.api.ValidatorDelegations(
            QueryValidatorDelegationsRequest(validator_addr=validator_addr)
        )

    def query_validator_unbonding_delegations(
        self, validator_addr: str
    ) -> QueryValidatorUnbondingDelegationsResponse:
        """Query ValidatorUnbondingDelegations."""
        return self.api.ValidatorUnbondingDelegations(
            QueryValidatorUnbondingDelegationsRequest(validator_addr=validator_addr)
        )

    def query_unbonding_delegation(
        self, validator_addr: str, delegator_addr: str
    ) -> QueryUnbondingDelegationResponse:
        """Query UnbondingDelegation."""
        return self.api.UnbondingDelegation(
            QueryUnbondingDelegationRequest(
                validator_addr=validator_addr, delegator_addr=delegator_addr
            )
        )

    def query_delegator_delegations(
        self, delegator_addr: str
    ) -> QueryDelegatorDelegationsResponse:
        """Query DelegatorDelegations."""
        return self.api.DelegatorDelegations(
            QueryDelegatorDelegationsRequest(delegator_addr=delegator_addr)
        )

    def query_delegator_unbonding_delegations(
        self, delegator_addr: str
    ) -> QueryDelegatorUnbondingDelegationsResponse:
        """Query DelegatorUnbondingDelegations."""
        return self.api.DelegatorUnbondingDelegations(
            QueryDelegatorUnbondingDelegationsRequest(delegator_addr=delegator_addr)
        )

    def query_redelegations(self, delegator_addr: str) -> QueryRedelegationsResponse:
        """Query Redelegations."""
        return self.api.Redelegations(
            QueryRedelegationsRequest(delegator_addr=delegator_addr)
        )

    def query_delegator_validators(
        self, delegator_addr: str
    ) -> QueryDelegatorValidatorsResponse:
        """Query DelegatorValidators."""
        return self.api.DelegatorValidators(
            QueryDelegatorValidatorsRequest(delegator_addr=delegator_addr)
        )

    def query_delegator_validator(
        self, delegator_addr: str, validator_addr: str
    ) -> QueryDelegatorValidatorResponse:
        """Query DelegatorValidator."""
        return self.api.DelegatorValidator(
            QueryDelegatorValidatorRequest(
                delegator_addr=delegator_addr, validator_addr=validator_addr
            )
        )

    def query_historical_info(self, height: str) -> QueryHistoricalInfoResponse:
        """Query HistoricalInfo."""
        return self.api.HistoricalInfo(QueryHistoricalInfoRequest(height=height))

    def query_pool(self) -> QueryPoolResponse:
        """Query Pool."""
        return self.api.Pool(QueryPoolRequest())

    def query_params(self) -> QueryParamsResponse:
        """Query Params."""
        return self.api.Params(QueryParamsRequest())
