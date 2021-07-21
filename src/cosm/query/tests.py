from cosm.query.rest_client import QueryRestClient
from unittest import TestCase
from unittest.mock import Mock, patch
from requests import Session, Response


class QueryTests(TestCase):
    @patch("requests.session", spec=Session)
    def test_get_pass(self, session_mock):
        rest_address = "some url"
        client = QueryRestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "my weird url path"
        resp = Mock(spec=Response)
        resp.status_code = 200
        resp.content = "dfdffdss".encode(encoding="utf8")

        session_mock.return_value.get.return_value = resp
        client.get(request_url_path)
        session_mock.return_value.get.assert_called_once_with(
            url=rest_address + request_url_path
        )

    @patch("requests.session", spec=Session)
    def test_get_error(self, session_mock):
        rest_address = "some url"
        client = QueryRestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "my weird url path"
        resp = Mock(spec=Response)
        resp.status_code = 400
        resp.content = "dfdffdss".encode(encoding="utf8")

        session_mock.return_value.get.return_value = resp

        with self.assertRaises(Exception) as context:
            client.get(request_url_path)

        self.assertTrue("Error when sending a query request" in str(context.exception))
