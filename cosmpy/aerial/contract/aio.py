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

"""Asyncio-native CosmWasm contract functionality."""

import json
from typing import Any, Optional

from cosmpy.aerial.client.aio import (
    AsyncLedgerClient,
    prepare_and_broadcast_basic_transaction,
)
from cosmpy.aerial.contract.base import LedgerContractBase
from cosmpy.aerial.contract.base import compute_digest as _compute_digest
from cosmpy.aerial.tx import TxFee
from cosmpy.aerial.tx_helpers import AsyncSubmittedTx
from cosmpy.aerial.wallet import Wallet
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QueryCodesRequest


class AsyncLedgerContract(LedgerContractBase):
    """Asyncio-native ledger contract bound to an ``AsyncLedgerClient``."""

    def __init__(
        self,
        path: Optional[str],
        client: AsyncLedgerClient,
        address: Optional[Address] = None,
        digest: Optional[bytes] = None,
        schema_path: Optional[str] = None,
        code_id: Optional[int] = None,
    ):
        """Initialize without performing network I/O.

        Use :meth:`create` to resolve a code id from the contract digest during
        construction. Otherwise that lookup is performed lazily by ``deploy``.

        :param path: path to the contract binary
        :param client: async ledger client
        :param address: instantiated contract address, defaults to None
        :param digest: contract digest, defaults to None
        :param schema_path: path to contract schemas, defaults to None
        :param code_id: stored contract code id, defaults to None
        """
        super().__init__()
        self._init_contract(path, client, address, digest, schema_path, code_id)
        self._code_id_checked = code_id is not None or self._digest is None

    @classmethod
    async def create(
        cls,
        path: Optional[str],
        client: AsyncLedgerClient,
        address: Optional[Address] = None,
        digest: Optional[bytes] = None,
        schema_path: Optional[str] = None,
        code_id: Optional[int] = None,
    ) -> "AsyncLedgerContract":
        """Create a contract and resolve its code id by digest when needed."""
        contract = cls(path, client, address, digest, schema_path, code_id)
        await contract._ensure_code_id()
        return contract

    async def _ensure_code_id(self):
        if not self._code_id_checked and self._digest is not None:
            self._code_id = await self._find_contract_id_by_digest(self._digest)
            self._code_id_checked = True

    async def store(
        self,
        sender: Wallet,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> int:
        """Store the contract and return its code id."""
        tx = self._store_tx(sender)
        submitted_tx = await prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        )
        await submitted_tx.wait_to_complete()
        self._code_id = submitted_tx.contract_code_id
        self._code_id_checked = True
        if self._code_id is None:
            raise RuntimeError("Unable to extract contract code id")
        return self._code_id

    async def instantiate(
        self,
        args: Any,
        sender: Wallet,
        label: Optional[str] = None,
        fee: Optional[TxFee] = None,
        admin_address: Optional[Address] = None,
        funds: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> Address:
        """Instantiate the contract and return its address."""
        tx = self._instantiate_tx(args, sender, label, admin_address, funds)
        submitted_tx = await prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        )
        await submitted_tx.wait_to_complete()
        self._address = submitted_tx.contract_address
        if self._address is None:
            raise RuntimeError("Unable to extract contract address")
        return self._address

    async def upgrade(
        self,
        args: Any,
        sender: Wallet,
        new_path: str,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
        """Store new code and migrate the current contract to it."""
        if self._address is None:
            raise RuntimeError("Address was not set.")
        self._path = new_path
        self._digest = _compute_digest(new_path)
        new_code_id = await self.store(sender, fee)
        return await self.migrate(
            args, sender, new_code_id, fee=fee, timeout_height=timeout_height
        )

    async def migrate(
        self,
        args: Any,
        sender: Wallet,
        new_code_id: int,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
        """Migrate the current contract address to a new code id."""
        tx = self._migrate_tx(args, sender, new_code_id)
        submitted_tx = await prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        )
        return await submitted_tx.wait_to_complete()

    async def update_admin(
        self,
        sender: Wallet,
        new_admin: Optional[Address],
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
        """Update or clear the contract admin."""
        tx = self._update_admin_tx(sender, new_admin)
        submitted_tx = await prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        )
        return await submitted_tx.wait_to_complete()

    async def deploy(
        self,
        args: Any,
        sender: Wallet,
        label: Optional[str] = None,
        store_fee: Optional[TxFee] = None,
        instantiate_fee: Optional[TxFee] = None,
        admin_address: Optional[Address] = None,
        funds: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> Address:
        """Deploy the contract, reusing already stored code when available."""
        if self._address is not None and self._code_id is not None:
            return self._address
        if self._address is not None:
            raise RuntimeError("Contract address is set but code id is not")
        await self._ensure_code_id()
        if self._code_id is None:
            await self.store(sender, fee=store_fee)
        return await self.instantiate(
            args,
            sender,
            label=label,
            fee=instantiate_fee,
            admin_address=admin_address,
            funds=funds,
            timeout_height=timeout_height,
        )

    async def execute(
        self,
        args: Any,
        sender: Wallet,
        fee: Optional[TxFee] = None,
        funds: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> AsyncSubmittedTx:
        """Execute the contract."""
        tx = self._execute_tx(args, sender, funds)
        return await prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        )

    async def query(self, args: Any) -> Any:
        """Query the contract."""
        req = self._query_request(args)
        resp = await self._client.wasm.SmartContractState(req)
        return json.loads(resp.data)

    async def _find_contract_id_by_digest(self, digest: bytes) -> Optional[int]:
        pagination = None
        while True:
            resp = await self._client.wasm.Codes(
                QueryCodesRequest(pagination=pagination)
            )
            for code_info in resp.code_infos:
                if code_info.data_hash == digest:
                    return int(code_info.code_id)
            if not resp.pagination.next_key:
                return None
            pagination = PageRequest(key=resp.pagination.next_key)
