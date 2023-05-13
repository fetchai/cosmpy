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

"""Interface for the Wasm functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import (
    QueryAllContractStateRequest,
    QueryAllContractStateResponse,
    QueryCodeRequest,
    QueryCodeResponse,
    QueryCodesRequest,
    QueryCodesResponse,
    QueryContractHistoryRequest,
    QueryContractHistoryResponse,
    QueryContractInfoRequest,
    QueryContractInfoResponse,
    QueryContractsByCodeRequest,
    QueryContractsByCodeResponse,
    QueryRawContractStateRequest,
    QueryRawContractStateResponse,
    QuerySmartContractStateRequest,
    QuerySmartContractStateResponse,
)


class CosmWasm(ABC):
    """Wasm abstract class."""

    @abstractmethod
    def ContractInfo(
        self,
        request: QueryContractInfoRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryContractInfoResponse:
        """
        Get the contract meta data.

        :param request: QueryContractInfoRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryContractInfoResponse
        """

    @abstractmethod
    def ContractHistory(
        self,
        request: QueryContractHistoryRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryContractHistoryResponse:
        """
        Get the contract code history.

        :param request: QueryContractHistoryRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryContractHistoryResponse
        """

    @abstractmethod
    def ContractsByCode(
        self,
        request: QueryContractsByCodeRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryContractsByCodeResponse:
        """
        List all smart contracts for a code id.

        :param request: QueryContractsByCodeRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryContractsByCodeResponse
        """

    @abstractmethod
    def AllContractState(
        self,
        request: QueryAllContractStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryAllContractStateResponse:
        """
        Get all raw store data for a single contract.

        :param request: QueryAllContractStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryAllContractStateResponse
        """

    @abstractmethod
    def RawContractState(
        self,
        request: QueryRawContractStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryRawContractStateResponse:
        """
        Get single key from the raw store data of a contract.

        :param request: QueryRawContractStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryRawContractStateResponse
        """

    @abstractmethod
    def SmartContractState(
        self,
        request: QuerySmartContractStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QuerySmartContractStateResponse:
        """
        Get smart query result from the contract.

        :param request: QuerySmartContractStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QuerySmartContractStateResponse
        """

    @abstractmethod
    def Code(
        self,
        request: QueryCodeRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryCodeResponse:
        """
        Get the binary code and metadata for a singe wasm code.

        :param request: QueryCodeRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryCodeResponse
        """

    @abstractmethod
    def Codes(
        self,
        request: QueryCodesRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryCodesResponse:
        """
        Get the metadata for all stored wasm codes.

        :param request: QueryCodesRequest
        :param metadata: The metadata for the call or None. metadata are additional headers

        :return: QueryCodesResponse
        """
