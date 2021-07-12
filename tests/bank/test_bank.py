import unittest
from unittest.mock import patch
from cosm.bank.bank import Bank


class MockResponse:
    def __init__(self, status_code: int, json_output: str):
        self.status_code = status_code
        self.json_output = json_output

    def json(self) -> str:
        return self.json_output


class MockSession:
    def __init__(self, status_code: int, json_output: str):
        self.status_code = status_code
        self.json_output = json_output
        self.last_url = ""

    def get(self, url: str) -> MockResponse:
        self.last_url = url
        return MockResponse(self.status_code, self.json_output)


class BankTests(unittest.TestCase):
    def test_get_balance(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_balance("account", "denom") == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/balances/account/denom')

    def test_get_all_balances(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_all_balances("account") == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/balances/account')

    def test_get_total_supply(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_total_supply() == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/supply')

    def test_get_supply_of(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_supply_of("denom") == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/supply/denom')

    def test_get_denoms_metadata(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_denoms_metadata() == "OK")
            assert (session.last_url == '/cosmos/bank/v1beta1/denoms_metadata')

    def test_get_denoms_metadata(self):
        bank = Bank("rest_address")

        session = MockSession(200, "OK")
        with patch.object(bank.rest_api, '_session', session):
            assert (bank.get_metadata_of_denom("denom") == "OK")
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/denoms_metadata/denom')
