from abc import ABC, abstractmethod

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


class Staking(ABC):
    """Staking abstract class."""

    @abstractmethod
    def Validators(self, request: QueryValidatorsRequest) -> QueryValidatorsResponse:
        """Validators queries all validators that match the given status."""
        pass

    @abstractmethod
    def Validator(self, request: QueryValidatorRequest) -> QueryValidatorResponse:
        """Validator queries validator info for given validator address."""
        pass

    @abstractmethod
    def ValidatorDelegations(
        self, request: QueryValidatorDelegationsRequest
    ) -> QueryValidatorDelegationsResponse:
        """ValidatorDelegations queries delegate info for given validator."""
        pass

    @abstractmethod
    def ValidatorUnbondingDelegations(
        self, request: QueryValidatorUnbondingDelegationsRequest
    ) -> QueryValidatorUnbondingDelegationsResponse:
        """ValidatorUnbondingDelegations queries unbonding delegations of a validator."""
        pass

    @abstractmethod
    def Delegation(self, request: QueryDelegationRequest) -> QueryDelegationResponse:
        """Delegation queries delegate info for given validator delegator pair."""
        pass

    @abstractmethod
    def UnbondingDelegation(
        self, request: QueryUnbondingDelegationRequest
    ) -> QueryUnbondingDelegationResponse:
        """UnbondingDelegation queries unbonding info for given validator delegator pair."""
        pass

    @abstractmethod
    def DelegatorDelegations(
        self, request: QueryDelegatorDelegationsRequest
    ) -> QueryDelegatorDelegationsResponse:
        """DelegatorDelegations queries all delegations of a given delegator address."""
        pass

    @abstractmethod
    def DelegatorUnbondingDelegations(
        self, request: QueryDelegatorUnbondingDelegationsRequest
    ) -> QueryDelegatorUnbondingDelegationsResponse:
        """DelegatorUnbondingDelegations queries all unbonding delegations of a given delegator address."""
        pass

    @abstractmethod
    def Redelegations(
        self, request: QueryRedelegationsRequest
    ) -> QueryRedelegationsResponse:
        """Redelegations queries redelegations of given address."""
        pass

    @abstractmethod
    def DelegatorValidators(
        self, request: QueryDelegatorValidatorsRequest
    ) -> QueryDelegatorValidatorsResponse:
        """DelegatorValidators queries all validators info for given delegator address."""
        pass

    @abstractmethod
    def DelegatorValidator(
        self, request: QueryDelegatorValidatorRequest
    ) -> QueryDelegatorValidatorResponse:
        """DelegatorValidator queries validator info for given delegator validator pair."""
        pass

    @abstractmethod
    def HistoricalInfo(
        self, request: QueryHistoricalInfoRequest
    ) -> QueryHistoricalInfoResponse:
        """HistoricalInfo queries the historical info for given height."""
        pass

    @abstractmethod
    def Pool(self, request: QueryPoolRequest) -> QueryPoolResponse:
        """Pool queries the pool info."""
        pass

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Parameters queries the staking parameters."""
        pass
