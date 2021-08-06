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

"""Tests for the CosmWasm client module of the Clients Package."""

import base64
import json
import unittest

from google.protobuf.json_format import MessageToDict, ParseDict

from cosm.auth.interface import AuthInterface
from cosm.clients.signing_cosmwasm_client import SigningCosmWasmClient
from cosm.crypto.address import Address
from cosm.crypto.keypairs import PrivateKey
from cosm.tests.helpers import MockQueryRestClient
from cosm.tx.interface import TxInterface
from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)
from cosmos.base.v1beta1.coin_pb2 import Coin
from cosmos.tx.v1beta1.service_pb2 import (
    BroadcastTxRequest,
    BroadcastTxResponse,
    GetTxRequest,
    GetTxResponse,
    GetTxsEventRequest,
    GetTxsEventResponse,
    SimulateRequest,
    SimulateResponse,
)

CHAIN_ID = "testing"

PRIVATE_KEY = PrivateKey(
    bytes.fromhex("deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
)
ADDRESS_PK = Address(PRIVATE_KEY)
PUBLIC_KEY_PK_BASE64 = base64.b64encode(PRIVATE_KEY.public_key_bytes).decode()

ADDRESS_OTHER = "fetchaddressaddressaddressaddressaddressaddr"
ACCOUNT_NUMBER = 0
SEQUENCE = 1

GAS_LIMIT = 987654321

DENOM = "stake"
AMOUNT = "1234"
COINS = [Coin(amount=AMOUNT, denom=DENOM)]

WASM_MSG = {"key": "value"}
WASM_MSG_BASE64 = base64.b64encode(json.dumps(WASM_MSG).encode("UTF8")).decode()
CODE_ID = 42
ADDRESS_CONTRACT = "fetchcontractcontractcontractcontractcontrac"
LABEL = "label"
CONTRACT_FILENAME = "dummy_contract.wasm"
CONTRACT_BYTECODE = "H4sIAG4mDWEA/3N0cnYBAKUgF9sEAAAA"


class MockAuth(AuthInterface):
    def __init__(
        self,
        address: Address = ADDRESS_PK,
        account_number: str = ACCOUNT_NUMBER,
        sequence: str = SEQUENCE,
    ):
        """
        Mock Auth client
        :param address: Mock address to be returned in response
        :param account_number: Mock account_number to be returned in response
        :param sequence: Mock sequence to be returned in response
        """
        self.address = address
        self.account_number = account_number
        self.sequence = sequence

    def Account(self, request: QueryAccountRequest) -> QueryAccountResponse:
        """Queries account data - sequence, account_id, etc."""
        content = {
            "account": {
                "@type": "/cosmos.auth.v1beta1.BaseAccount",
                "address": str(self.address),
                "pub_key": {},
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            }
        }
        return ParseDict(content, QueryAccountResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Queries all parameters"""
        raise NotImplementedError("Method not implemented!")


class MockTx(TxInterface):
    def __init__(self):
        pass

    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        """Simulate executing a transaction to estimate gas usage."""
        raise NotImplementedError("Method not implemented!")

    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        """GetTx fetches a tx by hash."""

    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        """BroadcastTx broadcast transaction."""

    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        """GetTxsEvent fetches txs by event."""
        raise NotImplementedError("Method not implemented!")


class CosmWasmClientTests(unittest.TestCase):
    """Test case of CosmWasm client module."""

    @classmethod
    def setUpClass(cls):
        """Set up test case."""

        # Mock Auth response for __init__
        mock_auth = MockAuth(ADDRESS_PK, ACCOUNT_NUMBER, SEQUENCE)
        content = MessageToDict(
            mock_auth.Account(QueryAccountRequest(address=str(ADDRESS_PK)))
        )

        mock_rest_client = MockQueryRestClient(json.dumps(content))
        cls.signing_wasm_client = SigningCosmWasmClient(
            PRIVATE_KEY, mock_rest_client, CHAIN_ID
        )
        cls.signing_wasm_client.auth_client = mock_auth

    def test_init(self):
        """Test correct initialisation."""
        assert str(ADDRESS_PK) == str(self.signing_wasm_client.address)
        assert ACCOUNT_NUMBER == self.signing_wasm_client.account_number
        assert CHAIN_ID == self.signing_wasm_client.chain_id
        assert PRIVATE_KEY.public_key_bytes == self.signing_wasm_client.public_key_bytes
        assert PRIVATE_KEY == self.signing_wasm_client.private_key

    def test_get_packed_send_msg(self):
        """Test correct generation of packed send msg."""
        expected_result = {
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "fromAddress": str(ADDRESS_PK),
            "toAddress": str(ADDRESS_OTHER),
            "amount": [{"denom": DENOM, "amount": AMOUNT}],
        }

        msg = self.signing_wasm_client.get_packed_send_msg(
            ADDRESS_PK, ADDRESS_OTHER, COINS
        )
        assert MessageToDict(msg) == expected_result

    def test_get_packed_init_msg(self):
        """Test correct generation of packed instantiate msg."""
        expected_result = {
            "@type": "/cosmwasm.wasm.v1beta1.MsgInstantiateContract",
            "sender": str(ADDRESS_PK),
            "codeId": str(CODE_ID),
            "label": LABEL,
            "initMsg": WASM_MSG_BASE64,
            "funds": [{"denom": DENOM, "amount": AMOUNT}],
        }

        msg = self.signing_wasm_client.get_packed_init_msg(
            ADDRESS_PK, CODE_ID, WASM_MSG, LABEL, COINS
        )
        assert MessageToDict(msg) == expected_result

    def test_get_packed_exec_msg(self):
        """Test correct generation of packed execute msg."""
        expected_result = {
            "@type": "/cosmwasm.wasm.v1beta1.MsgExecuteContract",
            "sender": str(ADDRESS_PK),
            "contract": str(ADDRESS_CONTRACT),
            "msg": WASM_MSG_BASE64,
            "funds": [{"denom": DENOM, "amount": AMOUNT}],
        }

        msg = self.signing_wasm_client.get_packed_exec_msg(
            ADDRESS_PK, ADDRESS_CONTRACT, WASM_MSG, COINS
        )
        assert MessageToDict(msg) == expected_result

    def test_get_packed_store_msg(self):
        """Test correct generation of packed store msg."""
        expected_result = {
            "@type": "/cosmwasm.wasm.v1beta1.MsgStoreCode",
            "sender": str(ADDRESS_PK),
            "wasmByteCode": CONTRACT_BYTECODE,
        }

        msg = self.signing_wasm_client.get_packed_store_msg(
            ADDRESS_PK, CONTRACT_FILENAME
        )

        msg_dict = MessageToDict(msg)
        assert len(msg_dict) == len(expected_result)
        assert msg_dict["sender"] == expected_result["sender"]
        assert msg_dict["@type"] == expected_result["@type"]
        # wasmByteCode is non-deterministic
        assert len(msg_dict["wasmByteCode"]) > 28

    def test_generate_tx(self):
        """Test correct generation of Tx."""
        expected_result = {
            "body": {
                "messages": [
                    {
                        "@type": "/cosmos.bank.v1beta1.MsgSend",
                        "fromAddress": str(ADDRESS_PK),
                        "toAddress": str(ADDRESS_OTHER),
                        "amount": [{"denom": DENOM, "amount": AMOUNT}],
                    }
                ],
                "memo": LABEL,
            },
            "authInfo": {
                "signerInfos": [
                    {
                        "publicKey": {
                            "@type": "/cosmos.crypto.secp256k1.PubKey",
                            "key": PUBLIC_KEY_PK_BASE64,
                        },
                        "modeInfo": {"single": {"mode": "SIGN_MODE_DIRECT"}},
                        "sequence": str(SEQUENCE),
                    }
                ],
                "fee": {
                    "amount": [{"denom": DENOM, "amount": AMOUNT}],
                    "gasLimit": str(GAS_LIMIT),
                },
            },
        }

        msg = self.signing_wasm_client.get_packed_send_msg(
            ADDRESS_PK, ADDRESS_OTHER, COINS
        )
        tx = self.signing_wasm_client.generate_tx(
            [msg], [ADDRESS_PK], [PRIVATE_KEY.public_key_bytes], COINS, LABEL, GAS_LIMIT
        )

        assert MessageToDict(tx) == expected_result

    def test_sign_tx(self):
        """Test correct generation of Tx."""
        expected_result = {
            "body": {
                "messages": [
                    {
                        "@type": "/cosmos.bank.v1beta1.MsgSend",
                        "fromAddress": str(ADDRESS_PK),
                        "toAddress": str(ADDRESS_OTHER),
                        "amount": [{"denom": DENOM, "amount": AMOUNT}],
                    }
                ],
                "memo": LABEL,
            },
            "authInfo": {
                "signerInfos": [
                    {
                        "publicKey": {
                            "@type": "/cosmos.crypto.secp256k1.PubKey",
                            "key": PUBLIC_KEY_PK_BASE64,
                        },
                        "modeInfo": {"single": {"mode": "SIGN_MODE_DIRECT"}},
                        "sequence": str(SEQUENCE),
                    }
                ],
                "fee": {
                    "amount": [{"denom": DENOM, "amount": AMOUNT}],
                    "gasLimit": str(GAS_LIMIT),
                },
            },
            "signatures": [
                "N/S3QvMc3zvS9X3UW20hPLxbXW4zE+x1M60xKsf5jE9FO6Q7vcVgEVIOj43bGZxh2rAfXcwM5u+hC7qRxOSgtA=="
            ],
        }

        # Generate and sign transaction
        msg = self.signing_wasm_client.get_packed_send_msg(
            ADDRESS_PK, ADDRESS_OTHER, COINS
        )
        tx = self.signing_wasm_client.generate_tx(
            [msg], [ADDRESS_PK], [PRIVATE_KEY.public_key_bytes], COINS, LABEL, GAS_LIMIT
        )
        self.signing_wasm_client.sign_tx(tx)
        dict_tx = MessageToDict(tx)

        # Check if signature has correct length
        assert len(base64.b64decode(dict_tx["signatures"][0])) == 64
        # Replace with returned signature because signature is non-deterministic
        expected_result["signatures"] = dict_tx["signatures"]

        assert dict_tx == expected_result
