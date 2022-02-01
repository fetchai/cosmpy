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

from cosmpy.bank.rest_client import BankRestClient
from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger
from cosmpy.common.rest_client import RestClient
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from tests.integration.generic.config import (
    AMOUNT,
    BOB_ADDRESS,
    CHAIN_ID,
    COINS,
    CONTRACT_FILENAME,
    DENOM,
    GRPC_ENDPOINT_ADDRESS,
    LABEL,
    REST_ENDPOINT_ADDRESS,
    TOKEN_ID,
    VALIDATOR_ADDRESS,
    VALIDATOR_CRYPTO,
)
from tests.integration.generic.test_cases import FetchdTestCase


class FetchdQueriesTestCase(FetchdTestCase):
    """Test case for Fetchd node."""

    @staticmethod
    def perform_transfer_using_ledger(
        ledger: CosmosLedger, validator_crypto: CosmosCrypto
    ):
        """
        This method is used to perform ledger interaction test
        using CosmosLedger which can communicate via REST or gRPC interface.

        :param ledger: CosmosLedger
        :param validator_crypto: CosmosCrypto
        """

        # Get balances before transfer
        from_balance = ledger.get_balance(validator_crypto.get_address(), DENOM)
        balance_from_before = from_balance
        to_balance = ledger.get_balance(BOB_ADDRESS, DENOM)
        balance_to_before = to_balance

        # Generate, sign and broadcast send tokens transaction
        ledger.send_funds(validator_crypto, BOB_ADDRESS, COINS)

        # Get balances after transfer
        from_balance = ledger.get_balance(validator_crypto.get_address(), DENOM)
        balance_from_after = from_balance
        to_balance = ledger.get_balance(BOB_ADDRESS, DENOM)
        balance_to_after = to_balance

        # Check if balances changed
        assert balance_from_after == balance_from_before - AMOUNT
        assert balance_to_after == balance_to_before + AMOUNT

    @staticmethod
    def prepare_contract_using_ledger(
        ledger: CosmosLedger, validator_crypto: CosmosCrypto
    ):
        """
        This method is used to perform ERC1155 contract interaction test
        using CosmosLedger which can communicate via REST or gRPC interface

        :param ledger: CosmosLedger
        :param validator_crypto: CosmosCrypto
        """

        # Store contract
        code_id, _ = ledger.deploy_contract(validator_crypto, CONTRACT_FILENAME)

        # Init contract
        init_msg: Dict[str, Any] = {}
        contract_address, _ = ledger.instantiate_contract(
            validator_crypto, code_id, init_msg, LABEL
        )

        # Create token with ID TOKEN_ID
        create_single_msg = {
            "create_single": {
                "item_owner": str(validator_crypto.get_address()),
                "id": TOKEN_ID,
                "path": "some_path",
            }
        }
        _, err_code = ledger.execute_contract(
            validator_crypto, contract_address, create_single_msg
        )
        assert err_code == 0

        # Mint 1 token with ID TOKEN_ID and give it to validator
        mint_single_msg = {
            "mint_single": {
                "to_address": str(validator_crypto.get_address()),
                "id": TOKEN_ID,
                "supply": str(AMOUNT),
                "data": "some_data",
            },
        }
        _, err_code = ledger.execute_contract(
            validator_crypto, contract_address, mint_single_msg
        )
        assert err_code == 0

        # Query validator's balance of token TOKEN_ID
        msg = {
            "balance": {
                "address": str(validator_crypto.get_address()),
                "id": TOKEN_ID,
            }
        }
        res_query = ledger.query_contract_state(
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
        ledger = CosmosLedger(
            rest_node_address=REST_ENDPOINT_ADDRESS, chain_id=CHAIN_ID
        )
        res = ledger.get_balance(VALIDATOR_ADDRESS, DENOM)

        assert res >= 1000

    def test_send_native_tokens_using_client_rest(self):
        """Test if sending tokens over REST api using CosmWasmClient works correctly"""
        # Create client
        ledger = CosmosLedger(
            rest_node_address=REST_ENDPOINT_ADDRESS, chain_id=CHAIN_ID
        )
        self.perform_transfer_using_ledger(ledger, VALIDATOR_CRYPTO)

    def test_send_native_tokens_using_client_grpc(self):
        """Test if sending tokens over gRPC api using CosmWasmClient works correctly"""
        # Create client
        ledger = CosmosLedger(rpc_node_address=GRPC_ENDPOINT_ADDRESS, chain_id=CHAIN_ID)
        self.perform_transfer_using_ledger(ledger, VALIDATOR_CRYPTO)

    def test_contract_interaction_using_client_rest(self):
        """Test full interaction with ERC1155 contract via REST api using CosmWasmClient"""

        # Create client
        ledger = CosmosLedger(
            rest_node_address=REST_ENDPOINT_ADDRESS, chain_id=CHAIN_ID
        )
        self.prepare_contract_using_ledger(ledger, VALIDATOR_CRYPTO)

    def test_contract_interaction_using_client_grpc(self):
        """Test full interaction with ERC1155 contract via GRPC api using CosmWasmClient"""

        # Create client
        ledger = CosmosLedger(rpc_node_address=GRPC_ENDPOINT_ADDRESS, chain_id=CHAIN_ID)
        self.prepare_contract_using_ledger(ledger, VALIDATOR_CRYPTO)
