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

"""Conftest module."""

from typing import List

import pytest


def pytest_collection_modifyitems(config, items: List[pytest.Item]):
    """
    Modify items collection for pytest.

    :param items: list of items
    """

    # Remove third party tests from integration tests
    for item in items:
        if "third_party" in item.nodeid:
            item.add_marker(pytest.mark.thirdparty(reason="Third party tests"))
        if config.option.markexpr != "thirdparty":
            item.add_marker(pytest.mark.skip(reason="Skipped in integration tests"))
