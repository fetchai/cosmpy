# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
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


"""Test aerial ledger client."""


from c4epy.aerial.client import (
    DEFAULT_QUERY_INTERVAL_SECS,
    DEFAULT_QUERY_TIMEOUT_SECS,
    LedgerClient,
)
from c4epy.aerial.config import NetworkConfig


def test_ledger_client_timeouts():
    """Test ledger client query_interval_secs and query_timeout_secs options."""
    client = LedgerClient(NetworkConfig.chain4energy_stable_testnet())
    assert (
        client._query_interval_secs  # pylint: disable=protected-access
        == DEFAULT_QUERY_INTERVAL_SECS
    )
    assert (
        client._query_timeout_secs  # pylint: disable=protected-access
        == DEFAULT_QUERY_TIMEOUT_SECS
    )

    timeout = 100
    interval = 5000
    client = LedgerClient(
        NetworkConfig.chain4energy_stable_testnet(),
        query_interval_secs=interval,
        query_timeout_secs=timeout,
    )
    assert client._query_interval_secs == interval  # pylint: disable=protected-access
    assert client._query_timeout_secs == timeout  # pylint: disable=protected-access
