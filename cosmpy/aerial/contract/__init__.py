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

"""cosmwasm contract functionality."""

import json
from typing import Any, Optional

from cosmpy.aerial.client import (
    LedgerClient,
    TxFee,
    prepare_and_broadcast_basic_transaction,
)
from cosmpy.aerial.contract.base import LedgerContractBase
from cosmpy.aerial.contract.cosmwasm import (  # noqa: F401
    create_cosmwasm_clear_admin_msg,
    create_cosmwasm_execute_msg,
    create_cosmwasm_instantiate_msg,
    create_cosmwasm_migrate_msg,
    create_cosmwasm_store_code_msg,
    create_cosmwasm_update_admin_msg,
)
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.aerial.wallet import Wallet
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QueryCodesRequest


class LedgerContract(LedgerContractBase):
    """Ledger contract."""

    def __init__(
        self,
        path: Optional[str],
        client: LedgerClient,
        address: Optional[Address] = None,
        digest: Optional[bytes] = None,
        schema_path: Optional[str] = None,
        code_id: Optional[int] = None,
    ):
        """Initialize the Ledger contract.

        :param path: Path
        :param client: Ledger client
        :param address: address, defaults to None
        :param digest: digest, defaults to None
        :param schema_path: path to contract schema, defaults to None
        :param code_id: optional int. code id of the contract stored
        """
        super().__init__()
        self._init_contract(path, client, address, digest, schema_path, code_id)

        # attempt to look up the code id from the network by digest
        if not code_id and self._digest is not None:
            self._code_id = self._find_contract_id_by_digest(self._digest)
        else:
            self._code_id = code_id

    def store(
        self,
        sender: Wallet,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> int:
        """Store the contract.

        :param sender: sender wallet address
        :param fee: transaction fee, defaults to None
        :param memo: transaction memo, defaults to None
        :param timeout_height: timeout height, defaults to None
        :raises RuntimeError: Runtime error
        :return: code id
        """
        tx = self._store_tx(sender)

        submitted_tx = prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            memo=memo,
            timeout_height=timeout_height,
        ).wait_to_complete()

        # extract the code id
        self._code_id = submitted_tx.contract_code_id
        if self._code_id is None:
            raise RuntimeError("Unable to extract contract code id")

        return self._code_id

    def instantiate(
        self,
        args: Any,
        sender: Wallet,
        label: Optional[str] = None,
        fee: Optional[TxFee] = None,
        admin_address: Optional[Address] = None,
        funds: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> Address:
        """Instantiate the contract.

        :param args: args
        :param sender: sender wallet address
        :param label: label, defaults to None
        :param fee: transaction fee, defaults to None
        :param admin_address: admin address, defaults to None
        :param funds: funds, defaults to None
        :param timeout_height: timeout height, defaults to None
        :raises RuntimeError: Unable to extract contract code id

        :return: contract address
        """
        tx = self._instantiate_tx(args, sender, label, admin_address, funds)

        submitted_tx = prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        ).wait_to_complete()

        # store the contract address
        self._address = submitted_tx.contract_address
        if self._address is None:
            raise RuntimeError("Unable to extract contract code id")

        return self._address

    def upgrade(
        self,
        args: Any,
        sender: Wallet,
        new_path: str,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Store new contract code and migrate the current contract address.

        :param args: args
        :param sender: sender wallet address
        :param new_path: path to new contract
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None
        :raises RuntimeError: contract address is not set

        :return: transaction details broadcast
        """
        if self._address is None:
            raise RuntimeError("Address was not set.")

        self._path = new_path
        new_code_id = self.store(sender, fee)

        return self.migrate(
            args,
            sender,
            new_code_id,
            fee=fee,
            timeout_height=timeout_height,
        )

    def migrate(
        self,
        args: Any,
        sender: Wallet,
        new_code_id: int,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Migrate the current contract address to new code id.

        :param args: args
        :param sender: sender wallet address
        :param new_code_id: Code id of the newly deployed contract
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None

        :return: transaction details broadcast
        """
        tx = self._migrate_tx(args, sender, new_code_id)

        return prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        ).wait_to_complete()

    def update_admin(
        self,
        sender: Wallet,
        new_admin: Optional[Address],
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """Update/clear the admin of the contract.

        :param sender: sender wallet address
        :param new_admin: New admin address, None for clear admin
        :param fee: transaction fee, defaults to None
        :param timeout_height: timeout height, defaults to None

        :return: transaction details broadcast
        """
        tx = self._update_admin_tx(sender, new_admin)

        return prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        ).wait_to_complete()

    def deploy(
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
        """Deploy the contract.

        :param args: args
        :param sender: sender address
        :param label: label, defaults to None
        :param store_fee: Store transaction fee, defaults to None
        :param instantiate_fee: instantiate Transaction fee, defaults to None
        :param admin_address: admin address, defaults to None
        :param funds: funds, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: instantiate contract details
        """
        # in the case where the contract is already deployed
        if self._address is not None and self._code_id is not None:
            return self._address

        assert self._address is None

        if self._code_id is None:
            self.store(sender, fee=store_fee)

        assert self._code_id is not None

        return self.instantiate(
            args,
            sender,
            label=label,
            fee=instantiate_fee,
            admin_address=admin_address,
            funds=funds,
            timeout_height=timeout_height,
        )

    def execute(
        self,
        args: Any,
        sender: Wallet,
        fee: Optional[TxFee] = None,
        funds: Optional[str] = None,
        timeout_height: Optional[int] = None,
    ) -> SubmittedTx:
        """execute the contract.

        :param args: args
        :param sender: sender address
        :param fee: transaction fee, defaults to None
        :param funds: funds, defaults to None
        :param timeout_height: timeout height, defaults to None
        :return: transaction details broadcast
        """
        tx = self._execute_tx(args, sender, funds)

        return prepare_and_broadcast_basic_transaction(
            self._client,
            tx,
            sender,
            fee=fee,
            timeout_height=timeout_height,
        )

    def query(self, args: Any) -> Any:
        """Query on contract.

        :param args: args
        :return: query result
        """
        req = self._query_request(args)
        resp = self._client.wasm.SmartContractState(req)
        return json.loads(resp.data)

    def _find_contract_id_by_digest(self, digest: bytes) -> Optional[int]:
        code_id = None

        pagination = None
        while True:
            req = QueryCodesRequest(pagination=pagination)
            resp = self._client.wasm.Codes(req)
            for code_info in resp.code_infos:
                if code_info.data_hash == digest:
                    code_id = int(code_info.code_id)
                    break

            # exit the search loop if we have successfully found our code id
            if code_id is not None:
                break

            # exit the search loop when we can't iterate any further
            if len(resp.pagination.next_key) == 0:
                break

            # proceed to the next page
            pagination = PageRequest(key=resp.pagination.next_key)

        return code_id
