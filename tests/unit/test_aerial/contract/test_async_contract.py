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
"""Tests for the async ledger contract."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from cosmpy.aerial.contract.aio import AsyncLedgerContract
from cosmpy.aerial.wallet import LocalWallet


def test_create_finds_code_id_by_digest():
    """The async factory resolves already uploaded code."""
    digest = b"contract digest"
    client = Mock()
    client.wasm.Codes = AsyncMock(
        return_value=SimpleNamespace(
            code_infos=[SimpleNamespace(data_hash=digest, code_id=42)],
            pagination=SimpleNamespace(next_key=b""),
        )
    )

    contract = asyncio.run(AsyncLedgerContract.create(None, client, digest=digest))

    assert contract.code_id == 42
    client.wasm.Codes.assert_awaited_once()


def test_query_awaits_smart_contract_state():
    """Contract queries use the async wasm stub."""
    client = Mock()
    client.wasm.SmartContractState = AsyncMock(
        return_value=SimpleNamespace(data=b'{"answer": 42}')
    )
    address = LocalWallet.generate().address()
    contract = AsyncLedgerContract(None, client, address=address)

    assert asyncio.run(contract.query({"value": {}})) == {"answer": 42}
    request = client.wasm.SmartContractState.await_args.args[0]
    assert request.address == str(address)


def test_store_waits_for_transaction_completion():
    """Store waits for inclusion before extracting the code id."""
    sender = LocalWallet.generate()
    submitted = Mock()
    submitted.wait_to_complete = AsyncMock(return_value=submitted)
    submitted.contract_code_id = 7

    with patch(
        "cosmpy.aerial.contract.base.compute_digest", return_value=b"digest"
    ), patch("cosmpy.aerial.contract.base.create_cosmwasm_store_code_msg"), patch(
        "cosmpy.aerial.contract.aio.prepare_and_broadcast_basic_transaction",
        AsyncMock(return_value=submitted),
    ):
        # Recreate inside the patch so no real contract file is needed.
        contract = AsyncLedgerContract("contract.wasm", Mock())
        assert asyncio.run(contract.store(sender)) == 7

    submitted.wait_to_complete.assert_awaited_once()


def test_execute_returns_uncompleted_submitted_transaction():
    """Execute mirrors LedgerContract by returning immediately after broadcast."""
    sender = LocalWallet.generate()
    address = LocalWallet.generate().address()
    submitted = Mock()
    contract = AsyncLedgerContract(None, Mock(), address=address)

    with patch(
        "cosmpy.aerial.contract.aio.prepare_and_broadcast_basic_transaction",
        AsyncMock(return_value=submitted),
    ):
        assert asyncio.run(contract.execute({"run": {}}, sender)) is submitted
