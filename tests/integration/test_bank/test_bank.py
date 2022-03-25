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

from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from tests.integration.utils.testcase import IntegrationTestCase


class TestBank(IntegrationTestCase):
    def test_query_balance(self):
        alice = LocalWallet(PrivateKey())

        expected_amount = 5 * 10 ** 18
        expected_denom = "atestfet"

        self.fund_account(
            target=alice.address(),
            amount=expected_amount,
            denom=expected_denom,
        )

        res = self.client.query_bank_balance(alice.address(), expected_denom)
        assert res == expected_amount

    def test_transfer(self):
        alice = LocalWallet(PrivateKey())
        bob = LocalWallet(PrivateKey())

        expected_amount = 5 * 10 ** 18
        expected_denom = "atestfet"

        self.fund_account(
            target=alice.address(),
            amount=expected_amount,
            denom=expected_denom,
        )

        transfered_amount = 2 * 10 ** 18

        tx = self.client.send_tokens(
            destination=bob.address(),
            amount=transfered_amount,
            denom="atestfet",
            sender=alice,
        )
        tx.wait_to_complete()

        alice_balance = self.client.query_bank_balance(alice.address(), expected_denom)
        assert alice_balance == (expected_amount - transfered_amount)
        bob_balance = self.client.query_bank_balance(bob.address(), expected_denom)
        assert bob_balance == transfered_amount
