from cosm.query.rest_client import QueryRestClient
from unittest import TestCase
import mock


class BankTests(TestCase):
    @mock.patch("urllib.request.urlopen", autospec=True)
    def test_get(self, mock_urlopen):
        client = QueryRestClient("address")
        client.get("/request")

        self.assertEqual(mock_urlopen.call_args_list[0].args, ("address/request",))

    def test_get_url_error(self):
        client = QueryRestClient("http://127.0.0.1")
        try:
            client.get("/request")
        except RuntimeError as e:
            assert "URLError" in str(e)

    def test_get_value_error(self):
        client = QueryRestClient("address")
        try:
            client.get("/request")
        except RuntimeError as e:
            assert "unknown url type" in str(e)
