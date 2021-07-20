import unittest
from unittest.mock import patch
from cosm.bank.rest_client import BankRestClient

from cosmos.bank.v1beta1.query_pb2 import (
    QueryBalanceRequest,
    QueryBalanceResponse,
    QueryAllBalancesRequest,
    QueryAllBalancesResponse,
    QueryTotalSupplyRequest,
    QueryTotalSupplyResponse,
    QuerySupplyOfRequest,
    QuerySupplyOfResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryDenomMetadataRequest,
    QueryDenomMetadataResponse,
    QueryDenomsMetadataRequest,
    QueryDenomsMetadataResponse,
)

from cosmos.bank.v1beta1.bank_pb2 import Params, Metadata

from cosmos.base.v1beta1.coin_pb2 import Coin
from cosmos.base.query.v1beta1.pagination_pb2 import PageResponse

import json


class MockQueryRestClient:
    def __init__(self, content: str):
        self.content = content
        self.last_request = ""

    def query(self, request: str) -> str:
        self.last_request = request
        return self.content


class BankTests(unittest.TestCase):
    def test_query_balance(self):
        expected_response = QueryBalanceResponse(
            balance=Coin(denom="stake", amount="1234")
        )
        content = {"balance": {"denom": "stake", "amount": "1234"}}
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert (
                bank.Balance(QueryBalanceRequest(address="account", denom="denom"))
                == expected_response  # noqa W503
            )
            assert (
                mock_client.last_request
                == "/cosmos/bank/v1beta1/balances/account/denom"  # noqa W503
            )

    def test_query_all_balances(self):
        expected_response = QueryAllBalancesResponse(
            balances=[Coin(denom="stake", amount="1234")],
            pagination=PageResponse(next_key=None, total=0),
        )
        content = {
            "balances": [{"denom": "stake", "amount": "1234"}],
            "pagination": {"next_key": None, "total": 0},
        }
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert (
                bank.AllBalances(QueryAllBalancesRequest(address="account"))
                == expected_response  # noqa W503
            )
            assert mock_client.last_request == "/cosmos/bank/v1beta1/balances/account"

    def test_query_total_supply(self):
        expected_response = QueryTotalSupplyResponse(
            supply=[Coin(denom="stake", amount="1234")]
        )
        content = {"supply": [{"denom": "stake", "amount": "1234"}]}
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert bank.TotalSupply(QueryTotalSupplyRequest()) == expected_response
            assert mock_client.last_request == "/cosmos/bank/v1beta1/supply"

    def test_query_supply_of(self):
        expected_response = QuerySupplyOfResponse(
            amount=Coin(denom="stake", amount="1234")
        )
        content = {"amount": {"denom": "stake", "amount": "1234"}}
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert (
                bank.SupplyOf(QuerySupplyOfRequest(denom="denom")) == expected_response
            )
            assert mock_client.last_request == "/cosmos/bank/v1beta1/supply/denom"

    def test_query_params(self):
        expected_response = QueryParamsResponse(
            params=Params(default_send_enabled=True)
        )
        content = {"params": {"default_send_enabled": True}}
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert bank.Params(QueryParamsRequest()) == expected_response
            assert mock_client.last_request == "/cosmos/bank/v1beta1/params"

    def test_query_denoms_metadata(self):
        expected_response = QueryDenomsMetadataResponse(
            pagination=PageResponse(next_key=None, total=0)
        )
        content = {"metadatas": [], "pagination": {"next_key": None, "total": 0}}
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert (
                bank.DenomsMetadata(QueryDenomsMetadataRequest()) == expected_response
            )
            assert mock_client.last_request == "/cosmos/bank/v1beta1/denoms_metadata"

    def test_query_denom_metadata(self):
        expected_response = QueryDenomMetadataResponse(metadata=Metadata())
        content = {
            "metadata": {
                "base": "",
                "denom_units": [],
                "description": "",
                "display": "",
            }
        }
        mock_client = MockQueryRestClient(json.dumps(content))

        bank = BankRestClient("rest_address")

        with patch.object(bank, "_rest_api", mock_client):
            assert (
                bank.DenomMetadata(QueryDenomMetadataRequest(denom="denom"))
                == expected_response  # noqa W503
            )
            assert (
                mock_client.last_request
                == "/cosmos/bank/v1beta1/denoms_metadata/denom"  # noqa W503
            )
