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
import gzip
from typing import Any, Optional

from cosmpy.aerial.coins import parse_coins
from cosmpy.common.utils import json_encode
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmwasm.wasm.v1.tx_pb2 import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgStoreCode,
)


def create_cosmwasm_store_code_msg(
    contract_path: str, sender_address: Address
) -> MsgStoreCode:
    with open(contract_path, "rb") as contract_file:
        wasm_byte_code = gzip.compress(contract_file.read(), 9)

    msg = MsgStoreCode(
        sender=str(sender_address),
        wasm_byte_code=wasm_byte_code,
    )

    return msg


def create_cosmwasm_instantiate_msg(
    code_id: int,
    args: Any,
    label: str,
    sender_address: Address,
    funds: Optional[str] = None,
    admin_address: Optional[Address] = None,
) -> MsgInstantiateContract:
    msg = MsgInstantiateContract(
        sender=str(sender_address),
        code_id=code_id,
        msg=json_encode(args).encode("UTF8"),
        label=label,
    )

    if funds is not None:
        msg.funds.extend(parse_coins(funds))
    if admin_address is not None:
        msg.admin = str(admin_address)  # noqa

    return msg


def create_cosmwasm_execute_msg(
    sender_address: Address,
    contract_address: Address,
    args: Any,
    funds: Optional[str] = None,
) -> MsgExecuteContract:
    msg = MsgExecuteContract(
        sender=str(sender_address),
        contract=str(contract_address),
        msg=json_encode(args).encode("UTF8"),
    )
    if funds is not None:
        msg.funds.extend(parse_coins(funds))

    return msg
