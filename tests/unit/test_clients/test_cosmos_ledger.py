# # -*- coding: utf-8 -*-
# # ------------------------------------------------------------------------------
# #
# #   Copyright 2018-2021 Fetch.AI Limited
# #
# #   Licensed under the Apache License, Version 2.0 (the "License");
# #   you may not use this file except in compliance with the License.
# #   You may obtain a copy of the License at
# #
# #       http://www.apache.org/licenses/LICENSE-2.0
# #
# #   Unless required by applicable law or agreed to in writing, software
# #   distributed under the License is distributed on an "AS IS" BASIS,
# #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# #   See the License for the specific language governing permissions and
# #   limitations under the License.
# #
# # ------------------------------------------------------------------------------
#
# """Tests for the CosmosLedger client module of the Clients Package."""
#
# import base64
# import gzip
# import json
# import os
# import tempfile
# import unittest
# from typing import Optional
# from unittest.mock import patch
#
# from google.protobuf.json_format import MessageToDict, ParseDict
#
# from cosmpy.auth.interface import Auth
# from cosmpy.auth.rest_client import AuthRestClient
# from cosmpy.bank.rest_client import BankRestClient
# from cosmpy.clients.crypto import CosmosCrypto
# from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
# from cosmpy.crypto.address import Address
# from cosmpy.crypto.keypairs import PrivateKey
# from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
# from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import (
#     QueryAccountRequest,
#     QueryAccountResponse,
#     QueryParamsRequest,
#     QueryParamsResponse,
# )
# from cosmpy.protos.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse
# from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
# from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import (
#     BroadcastTxRequest,
#     BroadcastTxResponse,
#     GetTxRequest,
#     GetTxResponse,
#     GetTxsEventRequest,
#     GetTxsEventResponse,
#     SimulateRequest,
#     SimulateResponse,
# )
# from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import Tx
# from cosmpy.tx.interface import TxInterface
# from tests.helpers import MockRestClient
#
# # Private key
# PRIVATE_KEY = PrivateKey(
#     bytes.fromhex("deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
# )
#
# # Addresses
# ADDRESS_PK = Address(PRIVATE_KEY)
# ADDRESS_OTHER = "fetchaddressaddressaddressaddressaddressaddr"
#
# # Public keys
# PUBLIC_KEY_PK_BASE64 = base64.b64encode(PRIVATE_KEY.public_key_bytes).decode()
#
# # Node config
# CHAIN_ID = "testing"
#
# # Auth data
# ACCOUNT_NUMBER = 0
# SEQUENCE = 1
#
# # Tx params
# GAS_LIMIT = 987654321
# LABEL = "label"
#
# # Coins
# DENOM = "stake"
# AMOUNT = "1234"
# COINS = [Coin(amount=AMOUNT, denom=DENOM)]
#
# # CosmWasm
# WASM_MSG = {"key": "value"}
# WASM_MSG_BASE64 = base64.b64encode(json_encode(WASM_MSG).encode("UTF8")).decode()
# CODE_ID = 42
# CONTRACT_ADDRESS = "fetchcontractcontractcontractcontractcontrac"
# CONTRACT_FILENAME = "dummy_contract.wasm"
# CONTRACT_BYTECODE = b"ABCD"
#
#
# class MockAuth(Auth):
#     """Mock Auth client"""
#
#     def __init__(
#         self,
#         address: Address,
#         account_number: int,
#         sequence: int,
#     ):
#         """
#         Create mock Auth client
#
#         :param address: Mock address to be returned in response
#         :param account_number: Mock account_number to be returned in response
#         :param sequence: Mock sequence to be returned in response
#         """
#         self.address = address
#         self.account_number = account_number
#         self.sequence = sequence
#
#     def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
#         """Queries account data - sequence, account_id, etc."""
#         content = {
#             "account": {
#                 "@type": "/cosmos.auth.v1beta1.BaseAccount",
#                 "address": str(self.address),
#                 "pub_key": {},
#                 "account_number": str(self.account_number),
#                 "sequence": str(self.sequence),
#             }
#         }
#         return ParseDict(content, QueryAccountResponse())
#
#     def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
#         """Queries all parameters"""
#         raise NotImplementedError("Method not implemented!")
#
#
# class MockTx(TxInterface):
#     """Mock Tx client"""
#
#     def __init__(self, response_code: int):
#         """
#         Create mock Tx client
#
#         :param response_code: Code in GetTxResponse returned on GetTx call
#         """
#         self.response_code = response_code
#         self.last_broadcast_tx_request: Optional[BroadcastTxRequest] = None
#
#     def Simulate(self, request: SimulateRequest) -> SimulateResponse:
#         """Simulate executing a transaction to estimate gas usage."""
#         raise NotImplementedError("Method not implemented!")
#
#     def GetTx(self, request: GetTxRequest) -> GetTxResponse:
#         """GetTx fetches a tx by hash."""
#         return GetTxResponse()
#
#     def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
#         """BroadcastTx broadcast transaction."""
#         self.last_broadcast_tx_request = request
#         return BroadcastTxResponse(tx_response=TxResponse(code=self.response_code))
#
#     def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
#         """GetTxsEvent fetches txs by event."""
#         raise NotImplementedError("Method not implemented!")
#
#
# def mock_get_code_id(response: GetTxResponse) -> int:
#     """Get code id from store code transaction response"""
#     assert isinstance(response, GetTxResponse)
#     return CODE_ID
#
#
# def mock_get_contract_address(response: GetTxResponse) -> str:
#     """Get code id from store code transaction response"""
#     assert isinstance(response, GetTxResponse)
#     return CONTRACT_ADDRESS
#
#
# class CosmosLedgerTestCase(unittest.TestCase):
#     """Test case of CosmosLedger module."""
#
#     @classmethod
#     def setUpClass(cls):
#         """Set up test case."""
#
#         # Mock Auth response for __init__
#         mock_auth = MockAuth(ADDRESS_PK, ACCOUNT_NUMBER, SEQUENCE)
#         content = MessageToDict(
#             mock_auth.Account(QueryAccountRequest(address=str(ADDRESS_PK)))
#         )
#
#         mock_rest_client = MockRestClient(json_encode(content))
#         cls.crypto = CosmosCrypto(
#             private_key=PRIVATE_KEY, account_number=ACCOUNT_NUMBER
#         )
#         cls.ledger = CosmosLedger(
#             rest_node_address="some_rest_node_address", chain_id=CHAIN_ID
#         )
#         cls.ledger.auth_client = mock_auth
#         cls.ledger.rest_client = mock_rest_client
#
#     def test_init(self):
#         """Test correct initialisation."""
#         assert str(ADDRESS_PK) == str(self.crypto.get_address())
#         assert ACCOUNT_NUMBER == self.crypto.account_number
#         assert CHAIN_ID == self.ledger.chain_id
#         assert PRIVATE_KEY.public_key_bytes == self.crypto.get_pubkey_as_bytes()
#         assert PRIVATE_KEY == self.crypto.private_key
#
#     def test_get_packed_send_msg(self):
#         """Test correct generation of packed send msg."""
#         expected_result = {
#             "@type": "/cosmos.bank.v1beta1.MsgSend",
#             "fromAddress": str(ADDRESS_PK),
#             "toAddress": str(ADDRESS_OTHER),
#             "amount": [{"denom": DENOM, "amount": AMOUNT}],
#         }
#
#         msg = self.ledger.get_packed_send_msg(ADDRESS_PK, ADDRESS_OTHER, COINS)
#         assert MessageToDict(msg) == expected_result
#
#     def test_get_packed_init_msg(self):
#         """Test correct generation of packed instantiate msg."""
#         expected_result = {
#             "@type": "/cosmwasm.wasm.v1.MsgInstantiateContract",
#             "sender": str(ADDRESS_PK),
#             "codeId": str(CODE_ID),
#             "label": LABEL,
#             "msg": WASM_MSG_BASE64,
#             "funds": [{"denom": DENOM, "amount": AMOUNT}],
#         }
#
#         msg = self.ledger.get_packed_init_msg(
#             ADDRESS_PK, CODE_ID, WASM_MSG, LABEL, COINS
#         )
#         assert MessageToDict(msg) == expected_result
#
#     def test_get_packed_exec_msg(self):
#         """Test correct generation of packed execute msg."""
#         expected_result = {
#             "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
#             "sender": str(ADDRESS_PK),
#             "contract": str(CONTRACT_ADDRESS),
#             "msg": WASM_MSG_BASE64,
#             "funds": [{"denom": DENOM, "amount": AMOUNT}],
#         }
#
#         msg = self.ledger.get_packed_exec_msg(
#             ADDRESS_PK, CONTRACT_ADDRESS, WASM_MSG, COINS
#         )
#         assert MessageToDict(msg) == expected_result
#
#     def test_get_packed_store_msg(self):
#         """Test correct generation of packed store msg."""
#         with tempfile.NamedTemporaryFile(suffix=CONTRACT_FILENAME, delete=False) as tmp:
#             tmp.write(CONTRACT_BYTECODE)
#             tmp.flush()
#         msg = self.ledger.get_packed_store_msg(ADDRESS_PK, tmp.name)
#         os.unlink(tmp.name)
#
#         msg_dict = MessageToDict(msg)
#         assert len(msg_dict) == 3
#         assert msg_dict["@type"] == "/cosmwasm.wasm.v1.MsgStoreCode"
#         assert msg_dict["sender"] == str(ADDRESS_PK)
#         zipped_bytecode: bytes = base64.b64decode(msg_dict["wasmByteCode"])
#         original_bytecode: bytes = gzip.decompress(zipped_bytecode)
#         self.assertEqual(original_bytecode, CONTRACT_BYTECODE)
#
#     def test_generate_tx(self):
#         """Test correct generation of Tx."""
#         expected_result = {
#             "body": {
#                 "messages": [
#                     {
#                         "@type": "/cosmos.bank.v1beta1.MsgSend",
#                         "fromAddress": str(ADDRESS_PK),
#                         "toAddress": str(ADDRESS_OTHER),
#                         "amount": [{"denom": DENOM, "amount": AMOUNT}],
#                     }
#                 ],
#                 "memo": LABEL,
#             },
#             "authInfo": {
#                 "signerInfos": [
#                     {
#                         "publicKey": {
#                             "@type": "/cosmos.crypto.secp256k1.PubKey",
#                             "key": PUBLIC_KEY_PK_BASE64,
#                         },
#                         "modeInfo": {"single": {"mode": "SIGN_MODE_DIRECT"}},
#                         "sequence": str(SEQUENCE),
#                     }
#                 ],
#                 "fee": {
#                     "amount": [{"denom": DENOM, "amount": AMOUNT}],
#                     "gasLimit": str(GAS_LIMIT),
#                 },
#             },
#         }
#
#         msg = self.ledger.get_packed_send_msg(ADDRESS_PK, ADDRESS_OTHER, COINS)
#         tx = self.ledger.generate_tx(
#             [msg], [ADDRESS_PK], [PRIVATE_KEY.public_key_bytes], COINS, LABEL, GAS_LIMIT
#         )
#
#         assert MessageToDict(tx) == expected_result
#
#     def test_sign_tx(self):
#         """Test correct generation of Tx."""
#         expected_result = {
#             "body": {
#                 "messages": [
#                     {
#                         "@type": "/cosmos.bank.v1beta1.MsgSend",
#                         "fromAddress": str(ADDRESS_PK),
#                         "toAddress": str(ADDRESS_OTHER),
#                         "amount": [{"denom": DENOM, "amount": AMOUNT}],
#                     }
#                 ],
#                 "memo": LABEL,
#             },
#             "authInfo": {
#                 "signerInfos": [
#                     {
#                         "publicKey": {
#                             "@type": "/cosmos.crypto.secp256k1.PubKey",
#                             "key": PUBLIC_KEY_PK_BASE64,
#                         },
#                         "modeInfo": {"single": {"mode": "SIGN_MODE_DIRECT"}},
#                         "sequence": str(SEQUENCE),
#                     }
#                 ],
#                 "fee": {
#                     "amount": [{"denom": DENOM, "amount": AMOUNT}],
#                     "gasLimit": str(GAS_LIMIT),
#                 },
#             },
#             "signatures": [
#                 "N/S3QvMc3zvS9X3UW20hPLxbXW4zE+x1M60xKsf5jE9FO6Q7vcVgEVIOj43bGZxh2rAfXcwM5u+hC7qRxOSgtA=="
#             ],
#         }
#
#         # Generate and sign transaction
#         msg = self.ledger.get_packed_send_msg(ADDRESS_PK, ADDRESS_OTHER, COINS)
#         tx = self.ledger.generate_tx(
#             [msg], [ADDRESS_PK], [PRIVATE_KEY.public_key_bytes], COINS, LABEL, GAS_LIMIT
#         )
#         self.ledger.sign_tx(self.crypto, tx)
#         dict_tx = MessageToDict(tx)
#
#         # Check if signature has correct length
#         assert len(base64.b64decode(dict_tx["signatures"][0])) == 64
#         # Replace with returned signature because signature is non-deterministic
#         expected_result["signatures"] = dict_tx["signatures"]
#
#         assert dict_tx == expected_result
#
#     def test_broadcast_tx_success(self):
#         """Test broadcast Tx with positive result."""
#         tx = self.ledger.generate_tx([], [], [], COINS, LABEL, GAS_LIMIT)
#
#         mock_tx_client = MockTx(response_code=0)
#         self.ledger.tx_client = mock_tx_client
#
#         result = self.ledger.broadcast_tx(tx, 1)
#         self.assertIsInstance(result, GetTxResponse)
#
#     def test_broadcast_tx_fail(self):
#         """Test broadcast Tx with negative result."""
#         tx = self.ledger.generate_tx([], [], [], COINS, LABEL, GAS_LIMIT)
#
#         # Response code different from 0 means Tx error
#         mock_tx_client = MockTx(response_code=1)
#         self.ledger.tx_client = mock_tx_client
#
#         # Check if broadcasting fails
#         self.assertRaises(BroadcastException, self.ledger.broadcast_tx, tx, 0)
#
#     def test_send_tokens(self):
#         """Test send tokens method with positive result."""
#
#         mock_tx_client = MockTx(response_code=0)
#         self.ledger.tx_client = mock_tx_client
#
#         result = self.ledger.send_funds(self.crypto, ADDRESS_OTHER, COINS)
#         self.assertIsInstance(result, dict)
#
#         # Reconstruct original Tx from last tx request bytes
#         tx = Tx()
#         tx.ParseFromString(mock_tx_client.last_broadcast_tx_request.tx_bytes)
#
#         assert len(tx.body.messages) == 1
#         assert tx.body.messages[0].type_url == "/cosmos.bank.v1beta1.MsgSend"
#
#     def test_deploy_contract(self):
#         """Test deploy contract method with positive result."""
#
#         mock_tx_client = MockTx(response_code=0)
#         self.ledger.tx_client = mock_tx_client
#
#         with patch.object(self.ledger, "get_code_id", mock_get_code_id):
#             with tempfile.NamedTemporaryFile(
#                 suffix=CONTRACT_FILENAME, delete=False
#             ) as tmp:
#                 tmp.write(CONTRACT_BYTECODE)
#                 tmp.flush()
#             code_id, _ = self.ledger.deploy_contract(self.crypto, tmp.name)
#             os.unlink(tmp.name)
#
#         assert code_id == CODE_ID
#
#         # Reconstruct original Tx from last tx request bytes
#         tx = Tx()
#         tx.ParseFromString(mock_tx_client.last_broadcast_tx_request.tx_bytes)
#
#         assert len(tx.body.messages) == 1
#         assert tx.body.messages[0].type_url == "/cosmwasm.wasm.v1.MsgStoreCode"
#
#     def test_init_contract(self):
#         """Test init contract method with positive result."""
#
#         mock_tx_client = MockTx(response_code=0)
#         self.ledger.tx_client = mock_tx_client
#
#         with patch.object(
#             self.ledger, "get_contract_address", mock_get_contract_address
#         ):
#             contract_address, _ = self.ledger.instantiate_contract(
#                 self.crypto, CODE_ID, WASM_MSG, LABEL
#             )
#         assert contract_address == CONTRACT_ADDRESS
#
#         # Reconstruct original Tx from last tx request bytes
#         tx = Tx()
#         tx.ParseFromString(mock_tx_client.last_broadcast_tx_request.tx_bytes)
#
#         assert len(tx.body.messages) == 1
#         assert (
#             tx.body.messages[0].type_url == "/cosmwasm.wasm.v1.MsgInstantiateContract"
#         )
#
#     def test_execute_contract(self):
#         """Test execute contract method with positive result."""
#
#         mock_tx_client = MockTx(response_code=0)
#         self.ledger.tx_client = mock_tx_client
#
#         result = self.ledger.execute_contract(self.crypto, CONTRACT_ADDRESS, WASM_MSG)
#         assert result == ({}, 0)
#
#         # Reconstruct original Tx from last tx request bytes
#         tx = Tx()
#         tx.ParseFromString(mock_tx_client.last_broadcast_tx_request.tx_bytes)
#
#         assert len(tx.body.messages) == 1
#         assert tx.body.messages[0].type_url == "/cosmwasm.wasm.v1.MsgExecuteContract"
#
#     def test_get_code_id(self):
#         """Test get code id from response with positive result."""
#
#         raw_log_dict = [
#             {
#                 "events": [
#                     {},
#                     {
#                         "type": "message",
#                         "attributes": [
#                             {"key": "code_id", "value": str(CODE_ID)},
#                         ],
#                     },
#                 ]
#             }
#         ]
#
#         tx_response = GetTxResponse()
#         tx_response.tx_response.raw_log = json_encode(raw_log_dict)
#
#         result = self.ledger.get_code_id(tx_response)
#         assert result == CODE_ID
#
#     def test_get_contract_address(self):
#         """Test get contract address from response with positive result."""
#
#         raw_log_dict = [
#             {
#                 "events": [
#                     {
#                         "type": "wasm",
#                         "attributes": [
#                             {"key": "_contract_address", "value": CONTRACT_ADDRESS}
#                         ],
#                     },
#                 ]
#             }
#         ]
#
#         tx_response = GetTxResponse()
#         tx_response.tx_response.raw_log = json_encode(raw_log_dict)
#
#         result = self.ledger.get_contract_address(tx_response)
#         assert result == CONTRACT_ADDRESS
#
#     def test_get_balance(self):
#         """Test get balance for the positive result."""
#
#         content = {"balance": {"denom": "stake", "amount": "1234"}}
#
#         mock_rest_client = MockRestClient(json_encode(content))
#         self.ledger.bank_client = BankRestClient(mock_rest_client)
#         response = self.ledger.get_balance("address", "stake")
#
#         assert response == 1234
#         assert (
#             mock_rest_client.last_base_url == "/cosmos/bank/v1beta1/balances/address/"
#         )
#
#     def test_get_balances(self):
#         """Test get balances for the positive result."""
#
#         content = {
#             "balances": [{"denom": "stake", "amount": "1234"}],
#             "pagination": {"next_key": None, "total": 0},
#         }
#
#         mock_rest_client = MockRestClient(json_encode(content))
#         self.ledger.bank_client = BankRestClient(mock_rest_client)
#         response = self.ledger.get_balances("address")
#
#         assert str(response) == '[denom: "stake"\namount: "1234"\n]'
#         assert mock_rest_client.last_base_url == "/cosmos/bank/v1beta1/balances/address"
#
#     def test_query_account_data(self):
#         """Test query account data for the positive result."""
#
#         content = {
#             "account": {
#                 "@type": "/cosmos.auth.v1beta1.BaseAccount",
#                 "address": "fetch1h6974x4dspft29r9gyegtajyzaht2cdh0rt93w",
#                 "pub_key": {
#                     "@type": "/cosmos.crypto.secp256k1.PubKey",
#                     "key": "A2BjpEo54gBpulf9CrA+6tGBASFC8okaO1DYTimk/Jwp",
#                 },
#                 "account_number": "0",
#                 "sequence": "1",
#             }
#         }
#         account_response = ParseDict(content, QueryAccountResponse())
#
#         account = BaseAccount()
#         if account_response.account.Is(BaseAccount.DESCRIPTOR):
#             account_response.account.Unpack(account)
#
#         mock_rest_client = MockRestClient(json_encode(content))
#         self.ledger.auth_client = AuthRestClient(mock_rest_client)
#         response = self.ledger.query_account_data("address")
#
#         assert response == account
#         assert mock_rest_client.last_base_url == "/cosmos/auth/v1beta1/accounts/address"
#
#     def test_query_contract_state(self):
#         """Test query contract state for the positive result."""
#
#         raw_content = b'{"data": {"balance":"1"}}'
#         expected_response = {"balance": "1"}
#
#         mock_rest_client = MockRestClient(raw_content)
#         self.ledger.wasm_client = CosmWasmRestClient(mock_rest_client)
#         response = self.ledger.query_contract_state("fetchcontractaddress", {})
#
#         assert response == expected_response
#         assert (
#             mock_rest_client.last_base_url
#             == "/wasm/v1/contract/fetchcontractaddress/smart/e30="
#         )
