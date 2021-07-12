import unittest
from unittest.mock import patch
from cosm.bank.bank import Bank


class MockResponse:
    def __init__(self, status_code, json_output):
        self.status_code = status_code
        self.json_output = json_output

    def json(self):
        return self.json_output


class MockSession:
    def __init__(self, status_code, json_output):
        self.status_code = status_code
        self.json_output = json_output
        self.last_url = ""

    def get(self, url):
        self.last_url = url
        return MockResponse(self.status_code, self.json_output)


class BankTests(unittest.TestCase):
    def test_get_balance(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_balance("account", "denom") == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/balances/account/denom')
