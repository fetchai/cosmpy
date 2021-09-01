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

"""Module with Fetchd integration tests."""

from typing import Any, Dict

from grpc import insecure_channel

from cosmpy.bank.rest_client import BankRestClient
from cosmpy.clients.signing_cosmwasm_client import CosmWasmClient, SigningCosmWasmClient
from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from tests.integration.generic.config import (
    AMOUNT,
    BOB_ADDRESS,
    CHAIN_ID,
    COINS,
    CONTRACT_FILENAME,
    DENOM,
    GRPC_ENDPOINT_ADDRESS,
    REST_ENDPOINT_ADDRESS,
    TOKEN_ID,
    VALIDATOR_ADDRESS,
    VALIDATOR_PK,
)
from tests.integration.generic.test_cases import FetchdTestCase


class FetchdQueriesTestCase(FetchdTestCase):
    """Test case for Fetchd node."""

    @staticmethod
    def perform_transfer_using_signing_client(validator_client: SigningCosmWasmClient):
        """
        This method is used to perform ERC1155 contract interaction test
        using SigningCosmWasmClient which can communicate via REST or gRPC interface.

        :param validator_client: SigningCosmWasmClient
        """

        # Get balances before transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_before = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(Address(BOB_ADDRESS), DENOM)
        balance_to_before = int(to_balance.balance.amount)

        # Generate, sign and broadcast send tokens transaction
        validator_client.send_tokens(Address(BOB_ADDRESS), COINS)

        # Get balances after transfer
        from_balance = validator_client.get_balance(validator_client.address, DENOM)
        balance_from_after = int(from_balance.balance.amount)
        to_balance = validator_client.get_balance(Address(BOB_ADDRESS), DENOM)
        balance_to_after = int(to_balance.balance.amount)

        # Check if balances changed
        assert balance_from_after == balance_from_before - AMOUNT
        assert balance_to_after == balance_to_before + AMOUNT

    @staticmethod
    def prepare_contract_using_signing_client(validator_client: SigningCosmWasmClient):
        """
        This method is used to perform ERC1155 contract interaction test
        using SigningCosmWasmClient which can communicate via REST or gRPC interface

        :param validator_client: SigningCosmWasmClient
        """

        # Store contract
        code_id = validator_client.deploy_contract(CONTRACT_FILENAME)

        # Init contract
        init_msg: Dict[str, Any] = {}
        contract_address = validator_client.instantiate_contract(code_id, init_msg)

        # Create token with ID TOKEN_ID
        create_single_msg = {
            "create_single": {
                "item_owner": str(validator_client.address),
                "id": TOKEN_ID,
                "path": "some_path",
            }
        }
        res_create = validator_client.execute_contract(
            contract_address, create_single_msg
        )
        assert res_create.tx_response.code == 0

        # Mint 1 token with ID TOKEN_ID and give it to validator
        mint_single_msg = {
            "mint_single": {
                "to_address": str(validator_client.address),
                "id": TOKEN_ID,
                "supply": str(AMOUNT),
                "data": "some_data",
            },
        }
        res_mint = validator_client.execute_contract(contract_address, mint_single_msg)
        assert res_mint.tx_response.code == 0

        # Query validator's balance of token TOKEN_ID
        msg = {
            "balance": {
                "address": str(validator_client.address),
                "id": TOKEN_ID,
            }
        }
        res_query = validator_client.query_contract_state(
            contract_address=contract_address, msg=msg
        )

        # Check if balance of token with ID TOKEN_ID of validator is correct
        assert res_query["balance"] == str(AMOUNT)

    @staticmethod
    def test_query_balance_rest():
        """Test if getting balance using REST api works correctly"""
        bank = BankRestClient(RestClient(REST_ENDPOINT_ADDRESS))
        res = bank.Balance(
            QueryBalanceRequest(address=str(VALIDATOR_ADDRESS), denom=DENOM)
        )
        assert res.balance.denom == DENOM
        assert int(res.balance.amount) >= 1000

    @staticmethod
    def test_query_balance_client_rest():
        """Test if getting balance using REST api and CosmWasmClient works correctly"""
        rest_client = RestClient(REST_ENDPOINT_ADDRESS)
        client = CosmWasmClient(rest_client)
        res = client.get_balance(VALIDATOR_ADDRESS, DENOM)

        assert res.balance.denom == DENOM
        assert int(res.balance.amount) >= 1000

    def test_send_native_tokens_using_client_rest(self):
        """Test if sending tokens over REST api using CosmWasmClient works correctly"""
        # Create client
        channel = RestClient(REST_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)
        self.perform_transfer_using_signing_client(validator_client)

    def test_send_native_tokens_using_client_grpc(self):
        """Test if sending tokens over gRPC api using CosmWasmClient works correctly"""
        # Create client
        channel = insecure_channel(GRPC_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)
        self.perform_transfer_using_signing_client(validator_client)

    def test_contract_interaction_using_client_rest(self):
        """Test full interaction with ERC1155 contract via REST api using CosmWasmClient"""

        # Create client
        channel = RestClient(REST_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)
        self.prepare_contract_using_signing_client(validator_client)

    def test_contract_interaction_using_client_grpc(self):
        """Test full interaction with ERC1155 contract via GRPC api using CosmWasmClient"""

        # Create client
        channel = insecure_channel(GRPC_ENDPOINT_ADDRESS)
        validator_client = SigningCosmWasmClient(VALIDATOR_PK, channel, CHAIN_ID)
        self.prepare_contract_using_signing_client(validator_client)
