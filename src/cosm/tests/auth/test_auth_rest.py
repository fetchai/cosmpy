import unittest
from unittest.mock import patch
from cosm.auth.auth_h import AuthWrapper
from cosm.auth.auth_rest import AuthRest

from cosmos.auth.v1beta1.query_pb2 import QueryAccountResponse, QueryParamsResponse
from google.protobuf.json_format import ParseDict

import json


class MockResponse:
    def __init__(self, status_code: int, content: str):
        self.status_code = status_code
        self.content = content


class MockSession:
    def __init__(self, status_code: int, content: str):
        self.status_code = status_code
        self.content = content
        self.last_url = ""

    def get(self, url: str) -> MockResponse:
        self.last_url = url
        return MockResponse(self.status_code, self.content)


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

        session = MockSession(200, json.dumps(content))

        auth = AuthWrapper(AuthRest("rest_address"))

        with patch.object(auth.auth_api.rest_api, "_session", session):
            assert auth.query_account("address") == expected_response
            assert (
                session.last_url == "rest_address/cosmos/auth/v1beta1/accounts/address"
            )
