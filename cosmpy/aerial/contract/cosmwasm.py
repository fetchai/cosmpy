import gzip
import json
from typing import Any, Optional

from cosmpy.aerial.coins import parse_coins
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmwasm.wasm.v1.tx_pb2 import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract


def create_cosmwasm_store_code_msg(contract_path: str, sender_address: Address) -> MsgStoreCode:
    with open(contract_path, "rb") as contract_file:
        wasm_byte_code = gzip.compress(contract_file.read(), 9)

    msg = MsgStoreCode(
        sender=str(sender_address),
        wasm_byte_code=wasm_byte_code,
    )

    return msg


def create_cosmwasm_instantiate_msg(code_id: int, args: Any, label: str, sender_address: Address,
                                    funds: Optional[str] = None,
                                    admin_address: Optional[Address] = None) -> MsgInstantiateContract:
    msg = MsgInstantiateContract(
        sender=str(sender_address),
        code_id=code_id,
        msg=json.dumps(args).encode("UTF8"),
        label=label,
    )

    if funds is not None:
        msg.funds = parse_coins(funds)
    if admin_address is not None:
        msg.admin = str(admin_address)

    return msg


def create_cosmwasm_execute_msg(sender_address: Address, contract_address: Address, args: Any,
                                funds: Optional[str] = None) -> MsgExecuteContract:
    msg = MsgExecuteContract(
        sender=str(sender_address),
        contract=str(contract_address),
        msg=json.dumps(args).encode("UTF8"),
    )
    if funds is not None:
        msg.funds = parse_coins(funds)

    return msg
