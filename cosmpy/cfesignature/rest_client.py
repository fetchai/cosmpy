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

"""Implementation of cfesignature interface using REST."""

from google.protobuf.json_format import Parse

from cosmpy.cfesignature.interface import CfeSignature
from cosmpy.common.rest_client import RestClient
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


class CfeSignatureRestClient(CfeSignature):
    """cfeminter REST client."""

    API_URL = "/c4e/signature/v1beta1"

    def __init__(self, rest_api: RestClient):
        """
        Initialize signature rest client.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Parameters queries the parameters of the module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())

    def CreateReferenceId(self, request: QueryCreateReferenceIdRequest) -> QueryCreateReferenceIdResponse:
        """
        Queries a list of CreateReferenceId items.

        :param request: QueryCreateReferenceIdRequest

        :return: QueryCreateReferenceIdResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/create_reference_id/{request.creator}")
        return Parse(json_response, QueryCreateReferenceIdResponse())

    def CreateStorageKey(self, request: QueryCreateStorageKeyRequest) -> QueryCreateStorageKeyResponse:
        """
        Queries a list of CreateStorageKey items.

        :param request: QueryCreateStorageKeyRequest

        :return: QueryCreateStorageKeyResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/create_storage_key/{request.targetAccAddress}/{request.referenceId}")
        return Parse(json_response, QueryCreateStorageKeyResponse())

    def CreateReferencePayloadLink(self,
                                   request: QueryCreateReferencePayloadLinkRequest) -> QueryCreateReferencePayloadLinkResponse:
        """
        Queries a list of CreateReferencePayloadLink items.

        :param request: QueryCreateReferencePayloadLinkRequest

        :return: QueryCreateReferencePayloadLinkResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/create_reference_payload_link/{request.referenceId}/{request.payloadHash}")
        return Parse(json_response, QueryCreateReferencePayloadLinkResponse())

    def VerifySignature(self, request: QueryVerifySignatureRequest) -> QueryVerifySignatureResponse:
        """
        Queries a list of State items.

        :param request: QueryVerifySignatureRequest

        :return: QueryVerifySignatureResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/verify_signature/{request.referenceId}/{request.targetAccAddress}")
        return Parse(json_response, QueryVerifySignatureResponse())

    def GetAccountInfo(self, request: QueryGetAccountInfoRequest) -> QueryGetAccountInfoResponse:
        """
        Queries a list of GetAccountInfo items.

        :param request: QueryGetAccountInfoRequest

        :return: QueryGetAccountInfoResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/get_account_info/{request.accAddressString}")
        return Parse(json_response, QueryGetAccountInfoResponse())

    def VerifyReferencePayloadLink(self,
                                   request: QueryVerifyReferencePayloadLinkRequest) -> QueryVerifyReferencePayloadLinkResponse:
        """
        Queries a list of VerifyReferencePayloadLink items.

        :param request: QueryVerifyReferencePayloadLinkRequest

        :return: QueryVerifyReferencePayloadLinkResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/verify_reference_payload_link/{request.referenceId}/{request.payloadHash}")
        return Parse(json_response, QueryVerifyReferencePayloadLinkResponse())

    def GetReferencePayloadLink(self,
                                request: QueryGetReferencePayloadLinkRequest) -> QueryGetReferencePayloadLinkResponse:
        """
        Queries a list of GetReferencePayloadLink items.

        :param request: QueryGetReferencePayloadLinkRequest

        :return: QueryGetReferencePayloadLinkResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/get_reference_payload_link/{request.referenceId}")
        return Parse(json_response, QueryGetReferencePayloadLinkResponse())
