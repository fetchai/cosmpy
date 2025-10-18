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

"""Interface for the Staking functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

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
    QueryValidatorUnbondingDelegationsRequest,
    QueryValidatorUnbondingDelegationsResponse,
    QueryValidatorsRequest,
    QueryValidatorsResponse,
)


class Staking(ABC):
    """Staking abstract class."""

    @abstractmethod
    def Validators(
        self,
        request: QueryValidatorsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryValidatorsResponse:
        """
        Query all validators that match the given status.

        :param request: QueryValidatorsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryValidatorsResponse
        """

    @abstractmethod
    def Validator(
        self,
        request: QueryValidatorRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryValidatorResponse:
        """
        Query validator info for given validator address.

        :param request: QueryValidatorRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryValidatorResponse
        """

    @abstractmethod
    def ValidatorDelegations(
        self,
        request: QueryValidatorDelegationsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryValidatorDelegationsResponse:
        """
        Query delegate info for given validator.

        :param request: QueryValidatorDelegationsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryValidatorDelegationsResponse
        """

    @abstractmethod
    def ValidatorUnbondingDelegations(
        self,
        request: QueryValidatorUnbondingDelegationsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryValidatorUnbondingDelegationsResponse:
        """
        Query unbonding delegations of a validator.

         :param request: ValidatorUnbondingDelegations
         :param metadata: The metadata for the call or None. metadata are additional headers

         :return: QueryValidatorUnbondingDelegationsResponse
        """

    @abstractmethod
    def Delegation(
        self,
        request: QueryDelegationRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryDelegationResponse:
        """
        Query delegate info for given validator delegator pair.

        :param request: QueryDelegationRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryDelegationResponse
        """

    @abstractmethod
    def UnbondingDelegation(
        self,
        request: QueryUnbondingDelegationRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryUnbondingDelegationResponse:
        """
        UnbondingDelegation queries unbonding info for given validator delegator pair.

        :param request: QueryUnbondingDelegationRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryUnbondingDelegationResponse
        """

    @abstractmethod
    def DelegatorDelegations(
        self,
        request: QueryDelegatorDelegationsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryDelegatorDelegationsResponse:
        """
        DelegatorDelegations queries all delegations of a given delegator address.

        :param request: QueryDelegatorDelegationsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryDelegatorDelegationsResponse
        """

    @abstractmethod
    def DelegatorUnbondingDelegations(
        self,
        request: QueryDelegatorUnbondingDelegationsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryDelegatorUnbondingDelegationsResponse:
        """
        DelegatorUnbondingDelegations queries all unbonding delegations of a given delegator address.

        :param request: QueryDelegatorUnbondingDelegationsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryDelegatorUnbondingDelegationsResponse
        """

    @abstractmethod
    def Redelegations(
        self,
        request: QueryRedelegationsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryRedelegationsResponse:
        """
        Redelegations queries redelegations of given address.

        :param request: QueryRedelegationsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryRedelegationsResponse
        """

    @abstractmethod
    def DelegatorValidators(
        self,
        request: QueryDelegatorValidatorsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryDelegatorValidatorsResponse:
        """
        DelegatorValidators queries all validators info for given delegator address.

        :param request: QueryDelegatorValidatorsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryDelegatorValidatorsRequest
        """

    @abstractmethod
    def DelegatorValidator(
        self,
        request: QueryDelegatorValidatorRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryDelegatorValidatorResponse:
        """
        DelegatorValidator queries validator info for given delegator validator pair.

        :param request: QueryDelegatorValidatorRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryDelegatorValidatorResponse
        """

    @abstractmethod
    def HistoricalInfo(
        self,
        request: QueryHistoricalInfoRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryHistoricalInfoResponse:
        """
        HistoricalInfo queries the historical info for given height.

        :param request: QueryHistoricalInfoRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryHistoricalInfoResponse
        """

    @abstractmethod
    def Pool(
        self,
        request: QueryPoolRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPoolResponse:
        """
        Pool queries the pool info.

        :param request: QueryPoolRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryPoolResponse
        """

    @abstractmethod
    def Params(
        self,
        request: QueryParamsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryParamsResponse:
        """
        Parameters queries the staking parameters.

        :param request: QueryParamsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryParamsResponse
        """
