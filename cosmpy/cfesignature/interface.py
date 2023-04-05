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

"""Interface for the cfesignature functionality of Chain4energy."""

from abc import ABC, abstractmethod

from cosmpy.protos.c4echain.cfesignature.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
    QueryCreateReferenceIdRequest,
    QueryCreateReferenceIdResponse,
    QueryCreateStorageKeyRequest,
    QueryCreateStorageKeyResponse,
    QueryCreateReferencePayloadLinkRequest,
    QueryCreateReferencePayloadLinkResponse,
    QueryVerifySignatureRequest,
    QueryVerifySignatureResponse,
    QueryGetAccountInfoRequest,
    QueryGetAccountInfoResponse,
    QueryVerifyReferencePayloadLinkRequest,
    QueryVerifyReferencePayloadLinkResponse,
    QueryGetReferencePayloadLinkRequest,
    QueryGetReferencePayloadLinkResponse
)


class CfeSignature(ABC):
    """cfesignature abstract class."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Parameters queries the parameters of the module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """

    @abstractmethod
    def CreateReferenceId(self, request: QueryCreateReferenceIdRequest) -> QueryCreateReferenceIdResponse:
        """
        Queries a list of CreateReferenceId items.

        :param request: QueryCreateReferenceIdRequest

        :return: QueryCreateReferenceIdResponse
        """

    @abstractmethod
    def CreateStorageKey(self, request: QueryCreateStorageKeyRequest) -> QueryCreateStorageKeyResponse:
        """
        Queries a list of CreateStorageKey items.

        :param request: QueryCreateStorageKeyRequest

        :return: QueryCreateStorageKeyResponse
        """

    @abstractmethod
    def CreateReferencePayloadLink(self,
                                   request: QueryCreateReferencePayloadLinkRequest) -> QueryCreateReferencePayloadLinkResponse:
        """
        Queries a list of CreateReferencePayloadLink items.

        :param request: QueryCreateReferencePayloadLinkRequest

        :return: QueryCreateReferencePayloadLinkResponse
        """

    @abstractmethod
    def VerifySignature(self, request: QueryVerifySignatureRequest) -> QueryVerifySignatureResponse:
        """
        Queries a list of State items.

        :param request: QueryVerifySignatureRequest

        :return: QueryVerifySignatureResponse
        """

    @abstractmethod
    def GetAccountInfo(self, request: QueryGetAccountInfoRequest) -> QueryGetAccountInfoResponse:
        """
        Queries a list of GetAccountInfo items.

        :param request: QueryGetAccountInfoRequest

        :return: QueryGetAccountInfoResponse
        """

    @abstractmethod
    def VerifyReferencePayloadLink(self,
                                   request: QueryVerifyReferencePayloadLinkRequest) -> QueryVerifyReferencePayloadLinkResponse:
        """
        Queries a list of VerifyReferencePayloadLink items.

        :param request: QueryVerifyReferencePayloadLinkRequest

        :return: QueryVerifyReferencePayloadLinkResponse
        """

    @abstractmethod
    def GetReferencePayloadLink(self,
                                request: QueryGetReferencePayloadLinkRequest) -> QueryGetReferencePayloadLinkResponse:
        """
        Queries a list of GetReferencePayloadLink items.

        :param request: QueryGetReferencePayloadLinkRequest

        :return: QueryGetReferencePayloadLinkResponse
        """
