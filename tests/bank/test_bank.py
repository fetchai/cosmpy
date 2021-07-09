import unittest
import mock
from cosm.bank.bank import Bank


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class BankTests(unittest.TestCase):

    @mock.patch('requests.get', autospec=True)
    def test_get_balance(self, mock_requests_get):
        mock_requests_get.return_value = MockResponse("OK", 200)

        bank = Bank("rest_address")
        assert (bank.get_balance("account", "denom") == "OK")
        assert (mock_requests_get.call_args.kwargs == {
            'url': 'rest_address/cosmos/bank/v1beta1/balances/account/denom'})
