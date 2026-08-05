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

"""Shared contract state, validation, and message construction."""

import json
import os
from collections import UserString
from datetime import datetime
from typing import Any, Dict, Optional

from jsonschema import validate

from cosmpy.aerial.contract.cosmwasm import (
    create_cosmwasm_clear_admin_msg,
    create_cosmwasm_execute_msg,
    create_cosmwasm_instantiate_msg,
    create_cosmwasm_migrate_msg,
    create_cosmwasm_store_code_msg,
    create_cosmwasm_update_admin_msg,
)
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import Wallet
from cosmpy.common.utils import json_encode
from cosmpy.crypto.address import Address
from cosmpy.crypto.hashfuncs import sha256
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QuerySmartContractStateRequest


def compute_digest(path: str) -> bytes:
    """Compute a contract binary's digest."""
    with open(path, "rb") as input_file:
        return sha256(input_file.read())


def generate_label(digest: bytes) -> str:
    """Generate an identifiable contract label."""
    now = datetime.utcnow()
    return f"{digest.hex()[:14]}-{now.strftime('%Y%m%d%H%M%S')}"


def load_contract_schema(schema_path: str) -> Optional[Dict[Any, Any]]:
    """Load the JSON schemas in a directory."""
    if not os.path.isdir(schema_path):
        return None
    schema = {}
    for filename in os.listdir(schema_path):
        if filename.endswith(".json"):
            msg_name = os.path.splitext(os.path.basename(filename))[0]
            full_path = os.path.join(schema_path, filename)
            with open(full_path, "r", encoding="utf-8") as schema_file:
                schema[msg_name] = json.load(schema_file)
    return schema


class LedgerContractBase(UserString):
    """Common functionality independent of the client's I/O model."""

    def __init__(self):
        # pylint: disable=super-init-not-called
        # UserString.__init__ assigns self.data, which is a read-only property
        # here (it returns self.address), so it cannot be called.
        self._path: Optional[str] = None
        self._client: Any = None
        self._address: Optional[Address] = None
        self._digest: Optional[bytes] = None
        self._code_id: Optional[int] = None
        self._schema: Optional[Dict[Any, Any]] = None
        self._instantiate_schema: Optional[Dict[str, Any]] = None
        self._query_schema: Optional[Dict[str, Any]] = None
        self._execute_schema: Optional[Dict[str, Any]] = None
        self._migrate_schema: Optional[Dict[str, Any]] = None

    def _init_contract(
        self,
        path: Optional[str],
        client: Any,
        address: Optional[Address],
        digest: Optional[bytes],
        schema_path: Optional[str],
        code_id: Optional[int],
    ):
        self._path = path
        self._client = client
        self._address = address
        self._load_schema(schema_path)
        self._digest = compute_digest(path) if path is not None else digest
        self._code_id = code_id

    @property
    def path(self) -> Optional[str]:
        """Get the contract path."""
        return self._path

    @property
    def digest(self) -> Optional[bytes]:
        """Get the contract digest."""
        return self._digest

    @property
    def code_id(self) -> Optional[int]:
        """Get the stored contract code id."""
        return self._code_id

    @property
    def address(self) -> Optional[Address]:
        """Get the instantiated contract address."""
        return self._address

    def _store_tx(self, sender: Wallet) -> Transaction:
        if self._path is None:
            raise RuntimeError("Unable to upload code, no contract provided")
        tx = Transaction()
        tx.add_message(create_cosmwasm_store_code_msg(self._path, sender.address()))
        return tx

    def _instantiate_tx(
        self,
        args: Any,
        sender: Wallet,
        label: Optional[str],
        admin_address: Optional[Address],
        funds: Optional[str],
    ) -> Transaction:
        if self._code_id is None:
            raise RuntimeError("Code id was not set.")
        self._validate(args, self._instantiate_schema)
        label = label or generate_label(
            self._digest or str(self._code_id).encode("utf-8")
        )
        tx = Transaction()
        tx.add_message(
            create_cosmwasm_instantiate_msg(
                self._code_id,
                args,
                label,
                sender.address(),
                admin_address=admin_address,
                funds=funds,
            )
        )
        return tx

    def _migrate_tx(self, args: Any, sender: Wallet, code_id: int) -> Transaction:
        if self._address is None:
            raise RuntimeError("Address was not set.")
        self._validate(args, self._migrate_schema)
        tx = Transaction()
        tx.add_message(
            create_cosmwasm_migrate_msg(code_id, args, self._address, sender.address())
        )
        return tx

    def _update_admin_tx(
        self, sender: Wallet, new_admin: Optional[Address]
    ) -> Transaction:
        if self._address is None:
            raise RuntimeError("Address was not set.")
        msg = (
            create_cosmwasm_clear_admin_msg(sender.address(), self._address)
            if new_admin is None
            else create_cosmwasm_update_admin_msg(
                sender.address(), self._address, new_admin
            )
        )
        tx = Transaction()
        tx.add_message(msg)
        return tx

    def _execute_tx(
        self, args: Any, sender: Wallet, funds: Optional[str]
    ) -> Transaction:
        if self._address is None:
            raise RuntimeError("Contract appears not to be deployed currently")
        self._validate(args, self._execute_schema)
        tx = Transaction()
        tx.add_message(
            create_cosmwasm_execute_msg(sender.address(), self._address, args, funds)
        )
        return tx

    def _query_request(self, args: Any) -> QuerySmartContractStateRequest:
        if self._address is None:
            raise RuntimeError("Contract appears not to be deployed currently")
        self._validate(args, self._query_schema)
        return QuerySmartContractStateRequest(
            address=str(self._address), query_data=json_encode(args).encode("UTF8")
        )

    @staticmethod
    def _validate(args: Any, schema: Optional[Dict[str, Any]]):
        if schema is not None:
            validate(args, schema)

    def _load_schema(self, schema_path: Optional[str]):
        self._schema = load_contract_schema(schema_path) if schema_path else None
        self._instantiate_schema = None
        self._query_schema = None
        self._execute_schema = None
        self._migrate_schema = None
        for msg_type, schema in (self._schema or {}).items():
            for name in ("instantiate", "query", "execute", "migrate"):
                if name in msg_type:
                    setattr(self, f"_{name}_schema", schema)
                    break

    @property
    def data(self):
        """Return the address for string-like compatibility."""
        return self.address

    def __json__(self):
        """Return the string representation for JSON serialization."""
        return str(self)
