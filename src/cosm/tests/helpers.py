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

"""Helpers methods and classes for testing."""

from typing import List, Optional

from google.protobuf.descriptor import Descriptor


class MockRestClient:
    """Mock RestClient"""

    def __init__(self, content: str):
        """Initialize."""
        self.content = content
        self.last_base_url: Optional[str] = None
        self.last_request: Optional[Descriptor] = None
        self.last_used_params: Optional[List[str]] = None

    def get(
        self,
        url_base_path: str,
        request: Descriptor,
        used_params: Optional[List[str]] = None,
    ) -> str:
        """Handle GET request."""
        self.last_base_url = url_base_path
        self.last_request = request
        self.last_used_params = used_params
        return self.content
