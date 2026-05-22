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

"""gRPC stub wrapper for request-scoped query context."""

from typing import Any

from cosmpy.aerial.grpc.rpc_wrapper import RpcMethodWrapper


class StubWrapper:
    """Wrap a generated gRPC query stub to support query context."""

    def __init__(self, stub: Any):
        """
        Init gRPC stub wrapper.

        :param stub: generated gRPC stub
        """
        self._stub = stub

    def __getattr__(self, name: str) -> Any:
        """Forward non-callable attributes and wrap RPC methods."""
        attr = getattr(self._stub, name)
        return RpcMethodWrapper(attr) if callable(attr) else attr
