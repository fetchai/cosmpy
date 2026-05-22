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

"""gRPC RPC method wrappers for request-scoped query context."""

from typing import Any, Callable, Optional

from cosmpy.aerial.query_context import ResponseQueryContext
from cosmpy.common.rest_client import COSMOS_BLOCK_HEIGHT_HEADER


def _request_height(ctx: Optional[ResponseQueryContext]) -> Optional[int]:
    """Get requested query height from a query context."""
    return getattr(ctx, "request_height", None) if ctx is not None else None


def _metadata_height(metadata: Any) -> Optional[int]:
    """Extract Cosmos block height from gRPC metadata."""
    for key, value in metadata or []:
        if key.lower() == COSMOS_BLOCK_HEIGHT_HEADER:
            return int(value)
    return None


class RpcMethodWrapper:
    """Wrap one gRPC RPC method to support query context."""

    def __init__(self, rpc: Callable):
        """
        Init RPC method wrapper.

        :param rpc: gRPC RPC method
        """
        self._rpc = rpc

    def __call__(
        self,
        request: Any,
        *,
        ctx: Optional[ResponseQueryContext] = None,
        metadata=None,
        **kwargs,
    ):
        """
        Call wrapped RPC method.

        :param request: RPC request
        :param ctx: optional query context
        :param metadata: optional gRPC metadata
        :param kwargs: additional gRPC call arguments
        :return: RPC response
        """
        request_height = _request_height(ctx)
        metadata = list(metadata or [])

        if request_height is not None:
            metadata.append((COSMOS_BLOCK_HEIGHT_HEADER, str(request_height)))

        if ctx is None:
            return self._rpc(request, metadata=metadata or None, **kwargs)

        response, call = self._rpc.with_call(
            request, metadata=metadata or None, **kwargs
        )
        response_height = _metadata_height(call.trailing_metadata())
        if response_height is None:
            response_height = _metadata_height(call.initial_metadata())
        ctx.response_height = response_height
        return response
