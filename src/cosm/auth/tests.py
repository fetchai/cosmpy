import json
import unittest

from google.protobuf.json_format import ParseDict

from cosm.auth.rest_client import AuthRestClient
from cosm.tests.helpers import MockQueryRestClient
from cosmos.auth.v1beta1.query_pb2 import (
    QueryAccountRequest,
    QueryAccountResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)


class AuthTests(unittest.TestCase):
    def test_query_account(self):
        content = {
            "account": {
                "@type": "/cosmos.auth.v1beta1.BaseAccount",
                "address": "fetch1h6974x4dspft29r9gyegtajyzaht2cdh0rt93w",
                "pub_key": {
                    "@type": "/cosmos.crypto.secp256k1.PubKey",
                    "key": "A2BjpEo54gBpulf9CrA+6tGBASFC8okaO1DYTimk/Jwp",
                },
                "account_number": "0",
                "sequence": "1",
            }
        }
        expected_response = ParseDict(content, QueryAccountResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        auth = AuthRestClient(mock_client)

        assert (
            auth.Account(QueryAccountRequest(address="address"))
            == expected_response  # noqa W503
        )
        assert mock_client.last_request == "/cosmos/auth/v1beta1/accounts/address"

    def test_query_params(self):
        content = {
            "params": {
                "max_memo_characters": 256,
                "tx_sig_limit": 7,
                "tx_size_cost_per_byte": 10,
                "sig_verify_cost_ed25519": 590,
                "sig_verify_cost_secp256k1": 1000,
            }
        }
        expected_response = ParseDict(content, QueryParamsResponse())

        mock_client = MockQueryRestClient(json.dumps(content))
        auth = AuthRestClient(mock_client)

        assert auth.Params(QueryParamsRequest()) == expected_response
        assert mock_client.last_request == "/cosmos/auth/v1beta1/params"
