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

"""Testcases for create instantiate and execute message."""

from cosmpy.aerial.contract import (
    create_cosmwasm_execute_msg,
    create_cosmwasm_instantiate_msg,
    create_cosmwasm_migrate_msg,
)
from cosmpy.crypto.address import Address


def test_create_instantiate_msg():
    """Test create instantiate message."""
    sender = Address("asi1r3d4azhlak4w00c5n02t9l35a3n6462vc388mu")
    msg = create_cosmwasm_instantiate_msg(
        1, {}, "init-label", sender, funds="10atestasi", admin_address=sender
    )

    assert msg.sender == str(sender)
    assert msg.code_id == 1
    assert msg.msg == b"{}"
    assert msg.label == "init-label"
    assert msg.admin == str(sender)
    assert len(msg.funds) == 1
    assert msg.funds[0].denom == "atestasi"
    assert msg.funds[0].amount == "10"


def test_create_execute_msg():
    """Test create execute message."""
    sender = Address("asi1r3d4azhlak4w00c5n02t9l35a3n6462vc388mu")
    contract = Address("asi1faucet4p2h432pxlh9ez8jfcl9jyr2ndyy338f")

    msg = create_cosmwasm_execute_msg(
        sender, contract, {}, funds="15atestasi,42another"
    )

    assert msg.sender == str(sender)
    assert msg.contract == str(contract)
    assert msg.msg == b"{}"
    assert len(msg.funds) == 2
    assert msg.funds[0].denom == "atestasi"
    assert msg.funds[0].amount == "15"
    assert msg.funds[1].denom == "another"
    assert msg.funds[1].amount == "42"


def test_create_migrate_msg():
    """Test create migrate message."""
    sender = Address("asi1r3d4azhlak4w00c5n02t9l35a3n6462vc388mu")
    contract_address = Address(
        "asi1j4t8vtg8dus7tpy6xrk9xnz5z4644qljeqtee2yw73ksvj3tqaeqsdrk98"
    )

    msg = create_cosmwasm_migrate_msg(1, {}, contract_address, sender)

    assert msg.sender == str(sender)
    assert msg.code_id == 1
    assert msg.contract == contract_address
    assert msg.sender == str(sender)
