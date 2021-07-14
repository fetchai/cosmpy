import unittest
from unittest.mock import patch
from cosm.bank.bank_h import Bank

from cosmos.bank.v1beta1.query_pb2 import QueryBalanceResponse, \
    QueryAllBalancesResponse, QueryTotalSupplyResponse, QuerySupplyOfResponse

from cosmos.base.v1beta1.coin_pb2 import Coin
from cosmos.base.query.v1beta1.pagination_pb2 import PageResponse

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


class BankTests(unittest.TestCase):
    def test_query_balance(self):
        expected_response = QueryBalanceResponse(balance=Coin(denom="stake", amount="1234"))
        content = {"balance":
            {
                "denom": "stake",
                "amount": "1234"
            }
        }
        session = MockSession(200, json.dumps(content))

        bank = Bank("rest_address")

        with patch.object(bank.bank_api.rest_api, '_session', session):
            assert (bank.query_balance("account", "denom") == expected_response)
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/balances/account/denom')

    def test_query_all_balances(self):
        expected_response = QueryAllBalancesResponse(balances=[Coin(denom="stake", amount="1234")],
                                                     pagination=PageResponse(next_key=None, total=0))
        content = {"balances":
            [{
                "denom": "stake",
                "amount": "1234"
            }],
            "pagination":
                {
                    "next_key": None,
                    "total": 0
                }
        }
        session = MockSession(200, json.dumps(content))

        bank = Bank("rest_address")

        with patch.object(bank.bank_api.rest_api, '_session', session):
            assert (bank.query_all_balances("account") == expected_response)
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/balances/account')

    def test_query_total_supply(self):
        expected_response = QueryTotalSupplyResponse(supply=[Coin(denom="stake", amount="1234")])
        content = {"supply":
            [{
                "denom": "stake",
                "amount": "1234"
            }]
        }
        session = MockSession(200, json.dumps(content))

        bank = Bank("rest_address")

        with patch.object(bank.bank_api.rest_api, '_session', session):
            assert (bank.query_total_supply() == expected_response)
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/supply')

    def test_query_supply_of(self):
        expected_response = QuerySupplyOfResponse(amount=Coin(denom="stake", amount="1234"))
        content = {"amount":
            {
                "denom": "stake",
                "amount": "1234"
            }
        }
        session = MockSession(200, json.dumps(content))

        bank = Bank("rest_address")

        with patch.object(bank.bank_api.rest_api, '_session', session):
            assert (bank.query_supply_of("denom") == expected_response)
            assert (session.last_url == 'rest_address/cosmos/bank/v1beta1/supply/denom')
