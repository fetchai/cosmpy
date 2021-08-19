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

"""Module with base test cases for integration tests."""

import time
from unittest import TestCase

from grpc import insecure_channel

from pycosm.bank.rest_client import BankRestClient
from pycosm.clients.signing_cosmwasm_client import CosmWasmClient, SigningCosmWasmClient
from pycosm.common.rest_client import RestClient
from pycosm.crypto.address import Address
from pycosm.crypto.keypairs import PrivateKey
from pycosm.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from pycosm.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from tests.integration.generic.fetchd_client import FetchdClient

# Denomination and amount of transferred tokens
DENOM = "stake"
AMOUNT = 1
COINS = [Coin(amount=str(AMOUNT), denom=DENOM)]

# Node config
GRPC_ENDPOINT_ADDRESS = "localhost:9090"
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"

# Private key of sender account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex("0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae")
)
VALIDATOR_ADDRESS = str(Address(VALIDATOR_PK))

# Private key of recipient account
BOB_PK = PrivateKey(
    bytes.fromhex("439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636")
)
BOB_ADDRESS = str(Address(BOB_PK))


class FetchdTestCase(TestCase):
    """Base test case for Fetchd node."""

    @classmethod
    def setUpClass(cls):
        """Set up Fetchd node for testing."""
        cls.client = FetchdClient()
        cls.client.run()

        # Wait for things to start working
        successful = False
        while not successful:
            time.sleep(5)

            try:
                rest_client = RestClient(REST_ENDPOINT_ADDRESS)
                client = CosmWasmClient(rest_client)
                res = client.get_balance(VALIDATOR_ADDRESS, DENOM)
                # Make sure that first block is minted
                if int(res.balance.amount) >= 1000:
                    successful = True
            except:
                continue

    @classmethod
    def tearDownClass(cls):
        """Teardown the Fetchd node."""
        cls.client.stop()

    @classmethod
    def test_query_balance_rest(cls):
        """Test if getting balance using REST api works correctly"""

        bank = BankRestClient(RestClient(REST_ENDPOINT_ADDRESS))
        res = bank.Balance(QueryBalanceRequest(address=VALIDATOR_ADDRESS, denom=DENOM))
        assert res.balance.denom == DENOM
        assert int(res.balance.amount) >= 1000

    @classmethod
    def test_query_balance_client_rest(cls):
        """Test if getting balance using REST api and CosmWasmClient works correctly"""

        rest_client = RestClient(REST_ENDPOINT_ADDRESS)
        client = CosmWasmClient(rest_client)
        res = client.get_balance(VALIDATOR_ADDRESS, DENOM)

        assert res.balance.denom == DENOM
        assert int(res.balance.amount) >= 1000

    @classmethod
    def test_send_native_tokens_using_client_rest(cls):
        """Test if sending tokens over REST api using CosmWasmClient works correctly"""

        # Create client
        channel = RestClient(REST_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)

        # Get balances before transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_before = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(BOB_ADDRESS, DENOM)
        balance_to_before = int(to_balance.balance.amount)

        # Generate, sign and broadcast send tokens transaction
        validator_client.send_tokens(BOB_ADDRESS, COINS)

        # Get balances after transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_after = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(BOB_ADDRESS, DENOM)
        balance_to_after = int(to_balance.balance.amount)

        # Check if balances changed
        assert balance_from_after == balance_from_before - AMOUNT
        assert balance_to_after == balance_to_before + AMOUNT

    @classmethod
    def test_send_native_tokens_using_client_grpc(cls):
        """Test if sending tokens over gRPC api using CosmWasmClient works correctly"""

        # Create client
        channel = insecure_channel(GRPC_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)

        # Address of recipient account
        BOB_ADDRESS = Address("fetch128r83uvcxns82535d3da5wmfvhc2e5mut922dw")

        # Get balances before transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_before = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(BOB_ADDRESS, DENOM)
        balance_to_before = int(to_balance.balance.amount)

        # Generate, sign and broadcast send tokens transaction
        validator_client.send_tokens(BOB_ADDRESS, COINS)

        # Get balances after transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_after = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(BOB_ADDRESS, DENOM)
        balance_to_after = int(to_balance.balance.amount)

        # Check if balances changed
        assert balance_from_after == balance_from_before - AMOUNT
        assert balance_to_after == balance_to_before + AMOUNT
