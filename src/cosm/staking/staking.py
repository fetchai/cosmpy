from cosm.query.rest_client import RestClient

# from cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
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


class Staking:
    """Staking module that wrapps REST queries."""

    def __init__(self, rest_address: str):
        """Initialize."""
        self.api = StakingRest(rest_address)

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


class StakingRest:
    """Staking REST API module."""

    API_URL = "/cosmos/staking/v1beta1"

    def __init__(self, rest_address: str):
        """Initialize."""
        self.rest_api = RestClient(rest_address)

    def Validators(self, request: QueryValidatorsRequest) -> QueryValidatorsResponse:
        """Validators queries all validators that match the given status."""
        json_response = self.rest_api.query(f"/{self.API_URL}/validators")
        return Parse(json_response, QueryValidatorsResponse())

    def Validator(self, request: QueryValidatorRequest) -> QueryValidatorResponse:
        """Validator queries validator info for given validator address."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/validators/{request.validator_addr}"
        )
        return Parse(json_response, QueryValidatorResponse())

    def ValidatorDelegations(
        self, request: QueryValidatorDelegationsRequest
    ) -> QueryValidatorDelegationsResponse:
        """ValidatorDelegations queries delegate info for given validator."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/validators/{request.validator_addr}/delegations"
        )
        return Parse(json_response, QueryValidatorDelegationsResponse())

    def ValidatorUnbondingDelegations(
        self, request: QueryValidatorUnbondingDelegationsRequest
    ) -> QueryValidatorUnbondingDelegationsResponse:
        """ValidatorUnbondingDelegations queries unbonding delegations of a validator."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/validators/{request.validator_addr}/unbonding_delegations"
        )
        return Parse(json_response, QueryValidatorUnbondingDelegationsResponse())

    def Delegation(self, request: QueryDelegationRequest) -> QueryDelegationResponse:
        """Delegation queries delegate info for given validator delegator pair."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/validators/{request.validator_addr}/delegations/{request.delegator_addr}"
        )
        return Parse(json_response, QueryDelegationResponse())

    def UnbondingDelegation(
        self, request: QueryUnbondingDelegationRequest
    ) -> QueryUnbondingDelegationResponse:
        """UnbondingDelegation queries unbonding info for given validator delegator pair."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/validators/{request.validator_addr}/delegations/{request.delegator_addr}/unbonding_delegation"
        )
        return Parse(json_response, QueryUnbondingDelegationResponse())

    def DelegatorDelegations(
        self, request: QueryDelegatorDelegationsRequest
    ) -> QueryDelegatorDelegationsResponse:
        """DelegatorDelegations queries all delegations of a given delegator address."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/delegations/{request.delegator_addr}"
        )
        return Parse(json_response, QueryDelegatorDelegationsResponse())

    def DelegatorUnbondingDelegations(
        self, request: QueryDelegatorUnbondingDelegationsRequest
    ) -> QueryDelegatorUnbondingDelegationsResponse:
        """DelegatorUnbondingDelegations queries all unbonding delegations of a given delegator address."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/delegators/{request.delegator_addr}/unbonding_delegations"
        )
        return Parse(json_response, QueryDelegatorUnbondingDelegationsResponse())

    def Redelegations(
        self, request: QueryRedelegationsRequest
    ) -> QueryRedelegationsResponse:
        """Redelegations queries redelegations of given address."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/delegators/{request.delegator_addr}/redelegations"
        )
        return Parse(json_response, QueryRedelegationsResponse())

    def DelegatorValidators(
        self, request: QueryDelegatorValidatorsRequest
    ) -> QueryDelegatorValidatorsResponse:
        """DelegatorValidators queries all validators info for given delegator address."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/delegators/{request.delegator_addr}/validators"
        )
        return Parse(json_response, QueryDelegatorValidatorsResponse())

    def DelegatorValidator(
        self, request: QueryDelegatorValidatorRequest
    ) -> QueryDelegatorValidatorResponse:
        """DelegatorValidator queries validator info for given delegator validator pair."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/delegators/{request.delegator_addr}/validators/{request.validator_addr}"
        )
        return Parse(json_response, QueryDelegatorValidatorResponse())

    def HistoricalInfo(
        self, request: QueryHistoricalInfoRequest
    ) -> QueryHistoricalInfoResponse:
        """HistoricalInfo queries the historical info for given height."""
        json_response = self.rest_api.query(
            f"/{self.API_URL}/historical_info/{request.height}"
        )
        return Parse(json_response, QueryHistoricalInfoResponse())

    def Pool(self, request: QueryPoolRequest) -> QueryPoolResponse:
        """Pool queries the pool info."""
        json_response = self.rest_api.query(f"/{self.API_URL}/pool")
        return Parse(json_response, QueryPoolResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Parameters queries the staking parameters."""
        json_response = self.rest_api.query(f"/{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())
