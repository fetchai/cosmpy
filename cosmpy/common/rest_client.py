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

"""Implementation of REST api client."""
import base64
import json
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import List, Optional
from urllib.parse import urlencode

import requests
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message

from cosmpy.aerial.query_context import ResponseQueryContext


COSMOS_BLOCK_HEIGHT_HEADER = "x-cosmos-block-height"


class RestClient:
    """REST api client."""

    def __init__(
        self,
        rest_address: str,
    ):
        """
        Create REST api client.

        :param rest_address: Address of REST node
        """
        self._session = requests.session()
        self.rest_address = rest_address
        self._query_ctx: ContextVar[Optional[ResponseQueryContext]] = ContextVar(
            "rest_query_context", default=None
        )

    @contextmanager
    def query_context(self, ctx: Optional[ResponseQueryContext]):
        """Temporarily set the current query context."""
        token: Optional[Token] = None
        try:
            token = self._query_ctx.set(ctx)
            yield
        finally:
            if token is not None:
                self._query_ctx.reset(token)

    @staticmethod
    def _request_height(ctx: Optional[ResponseQueryContext]) -> Optional[int]:
        """Get requested query height from a query context."""
        return getattr(ctx, "request_height", None) if ctx is not None else None

    @staticmethod
    def _response_height(response: requests.Response) -> Optional[int]:
        """Get response query height from response headers."""
        height = response.headers.get(COSMOS_BLOCK_HEIGHT_HEADER)
        if height is None:
            height = response.headers.get(f"grpc-metadata-{COSMOS_BLOCK_HEIGHT_HEADER}")
        return int(height) if height is not None else None

    def get(
        self,
        url_base_path: str,
        request: Optional[Message] = None,
        used_params: Optional[List[str]] = None,
        ctx: Optional[ResponseQueryContext] = None,
    ) -> bytes:
        """
        Send a GET request.

        :param url_base_path: URL base path
        :param request: Protobuf coded request
        :param used_params: Parameters to be removed from request after converting it to dict
        :param ctx: optional query context

        :raises RuntimeError: if response code is not 200

        :return: Content of response
        """
        url = self._make_url(
            url_base_path=url_base_path, request=request, used_params=used_params
        )

        ctx = ctx or self._query_ctx.get()
        request_height = self._request_height(ctx)
        request_kwargs = {"url": url}
        if request_height is not None:
            request_kwargs["headers"] = {
                COSMOS_BLOCK_HEIGHT_HEADER: str(request_height)
            }

        response = self._session.get(**request_kwargs)
        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a GET request.\n Response: {response.status_code}, {str(response.content)})"
            )
        if ctx is not None:
            ctx.response_height = self._response_height(response)
        return response.content

    def _make_url(
        self,
        url_base_path: str,
        request: Optional[Message] = None,
        used_params: Optional[List[str]] = None,
    ) -> str:
        """
        Construct URL for get request.

        :param url_base_path: URL base path
        :param request: Protobuf coded request
        :param used_params: Parameters to be removed from request after converting it to dict

        :return: URL string
        """
        json_request = MessageToDict(request) if request else {}

        # Remove params that are already in url_base_path
        for param in used_params or []:
            json_request.pop(param)

        url_encoded_request = self._url_encode(json_request)

        url = f"{self.rest_address}{url_base_path}"
        if url_encoded_request:
            url = f"{url}?{url_encoded_request}"

        return url

    def post(self, url_base_path: str, request: Message) -> bytes:
        """
        Send a POST request.

        :param url_base_path: URL base path
        :param request: Protobuf coded request

        :raises RuntimeError: if response code is not 200

        :return: Content of response
        """
        json_request = MessageToDict(request)

        # Workaround
        if "tx" in json_request:
            if "body" in json_request["tx"]:
                if "messages" in json_request["tx"]["body"]:
                    for message in json_request["tx"]["body"]["messages"]:
                        if "msg" in message:
                            message["msg"] = json.loads(
                                base64.b64decode(message["msg"])
                            )

        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = self._session.post(
            url=f"{self.rest_address}{url_base_path}",
            json=json_request,
            headers=headers,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a POST request.\n Request: {json_request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    @staticmethod
    def _url_encode(json_request):
        """A Custom URL encodes that breaks down nested dictionaries to match REST api format.

        It converts dicts from:
        {"pagination": {"limit": "1", "something": "2"},}

        To:
        {"pagination.limit": "1","pagination.something": "2"}


        :param json_request: JSON request

        :return: urlencoded json_request
        """  # noqa: D401
        for outer_k, outer_v in json_request.copy().items():
            if isinstance(outer_v, dict):
                for inner_k, inner_v in outer_v.items():
                    json_request[f"{outer_k}.{inner_k}"] = inner_v
                json_request.pop(outer_k)

        return urlencode(json_request, doseq=True)

    def __del__(self):
        """Destructor method."""
        self._session.close()
