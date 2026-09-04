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

"""Request-scoped query context helpers."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResponseQueryContext:
    """Response context populated with the block height used for a query."""

    response_height: Optional[int] = field(init=False, default=None)


@dataclass
class RequestQueryContext(ResponseQueryContext):
    """Request context for pinning a query to a block height."""

    request_height: int
