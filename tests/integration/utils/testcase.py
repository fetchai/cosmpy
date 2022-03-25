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

from unittest import TestCase

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
from tests.integration.utils.chain import Chain
from tests.integration.utils.container import Container


class IntegrationTestCase(TestCase):
    """Base integration test class."""

    @classmethod
    def setUpClass(cls):
        """Set up test network."""
        # key generated from fetchd, mnemonic set in entrypoint.sh
        # base64 of private key below is generated from `fetchd keys export <keyname> --unsafe --unarmored-hex | xxd -r -p | base64`
        # TODO: rework this once cosmpy have support for mnemonic/armored keys to avoid key duplication.
        cls._root_private_key = PrivateKey(
            "Zgm/iabapcyPBMsH4bEVVeIJQ0IxkD+9dfM2CK5I/6I="
        )

        cls.chain = Chain(Container())
        chain_status = cls.chain.start()

        cls.client = LedgerClient(
            NetworkConfig(
                chain_id=chain_status.chain_id,
                fee_denomination="atestfet",
                staking_denomination="atestfet",
                url=chain_status.grpc_endpoint,
                fee_minimum_gas_price=0,
            )
        )

    @classmethod
    def tearDownClass(cls):
        """Teardown the Fetchd node."""
        cls.chain.stop()

    def fund_account(self, target: Address, amount: int, denom: str) -> LocalWallet:
        """
        Transfers requested amount of denom from root account to target address.
        Note that the root account (the one identified by cls._root_private_key)
        must have funds available for the requested denomination.

        :param target: Address where the funds will be transfered to
        :param amount: Amount to be transfered
        :param denom: Token denomination to transfer
        """
        tx = self.client.send_tokens(
            destination=target,
            amount=amount,
            denom=denom,
            sender=LocalWallet(self._root_private_key),
        )
        tx.wait_to_complete()
