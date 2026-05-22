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

"""Query client wrappers for request-scoped query context."""

from contextlib import nullcontext
from typing import Any, Optional

from cosmpy.aerial.grpc.stub_wrapper import StubWrapper
from cosmpy.aerial.query_context import ResponseQueryContext
from cosmpy.common.rest_client import RestClient


def is_query_grpc_stub(stub: Any) -> bool:
    """Return true if a generated gRPC stub represents a Cosmos query service."""
    return str(getattr(stub.__class__, "__module__", "")).endswith(".query_pb2_grpc")


def wrap_query_client(client: Any) -> Any:
    """Wrap supported query clients with request-scoped query context support."""
    if is_query_grpc_stub(client):
        return StubWrapper(client)
    if _find_rest_client(client) is not None:
        return RestQueryClientWrapper(client)
    return NoopQueryClientWrapper(client)


def _find_rest_client(client: Any) -> Optional[RestClient]:
    """Find a RestClient held by a generated REST module client."""
    for value in vars(client).values():
        if isinstance(value, RestClient):
            return value
    return None


class RestQueryClientWrapper:
    """Wrap a REST module client to support query context without per-method code."""

    def __init__(self, client: Any):
        """
        Init REST query client wrapper.

        :param client: REST module client
        """
        self._client = client
        self._rest_client = _find_rest_client(client)

    def __getattr__(self, name: str) -> Any:
        """Forward non-callable attributes and wrap client methods."""
        attr = getattr(self._client, name)
        if not callable(attr):
            return attr

        def call_with_ctx(*args, ctx: Optional[ResponseQueryContext] = None, **kwargs):
            ctx_manager = (
                self._rest_client.query_context(ctx)
                if self._rest_client is not None and ctx is not None
                else nullcontext()
            )
            with ctx_manager:
                return attr(*args, **kwargs)

        return call_with_ctx


class NoopQueryClientWrapper:
    """Wrap clients so a ctx keyword does not break non-query calls."""

    def __init__(self, client: Any):
        """
        Init no-op query client wrapper.

        :param client: client instance
        """
        self._client = client

    def __getattr__(self, name: str) -> Any:
        """Forward non-callable attributes and ignore ctx for client methods."""
        attr = getattr(self._client, name)
        if not callable(attr):
            return attr

        def call_ignoring_ctx(
            *args, ctx: Optional[ResponseQueryContext] = None, **kwargs
        ):
            return attr(*args, **kwargs)

        return call_ignoring_ctx
