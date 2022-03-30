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

"""Tests for REST client."""

from unittest import TestCase
from unittest.mock import Mock, patch

from requests import Response, Session

from cosmpy.common.rest_client import RestClient


class QueryRestClientTestCase(TestCase):
    """Test case of REST client module."""

    @staticmethod
    @patch("requests.session", spec=Session)
    @patch("cosmpy.common.rest_client.MessageToDict")
    def test_get_pass(messageToDict_mock, session_mock):
        """
        Test get method for the positive result.

        :param messageToDict_mock: mock
        :param session_mock: mock
        """
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 200
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {
            "a": 1,
            "b": ["something", "else"],
            "some_dict": {"x": 1, "y": 2},
        }
        messageToDict_mock.return_value = request_json
        session_mock.return_value.get.return_value = resp
        client.get(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)

        expected_url = f"{rest_address}{request_url_path}?a=1&b=something&b=else&some_dict.x=1&some_dict.y=2"
        session_mock.return_value.get.assert_called_once_with(url=expected_url)

    @patch("requests.session", spec=Session)
    @patch("cosmpy.common.rest_client.MessageToDict")
    def test_get_error(self, messageToDict_mock, session_mock):
        """
        Test get method for the negative result.

        :param messageToDict_mock: mock
        :param session_mock: mock
        """

        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 400
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json
        session_mock.return_value.get.return_value = resp

        with self.assertRaises(Exception) as context:
            client.get(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)
        self.assertTrue("Error when sending a GET request" in str(context.exception))

    @staticmethod
    @patch("requests.session", spec=Session)
    @patch("cosmpy.common.rest_client.MessageToDict")
    def test_post_pass(messageToDict_mock, session_mock):
        """
        Test post method for the positive result.

        :param messageToDict_mock: mock
        :param session_mock: mock
        """

        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 200
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json

        session_mock.return_value.post.return_value = resp
        client.post(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)

        _, kwargs = session_mock.return_value.post.call_args
        headers = kwargs["headers"]
        assert (
            headers.items()
            >= {
                "Content-type": "application/json",
                "Accept": "application/json",
            }.items()
        )
        assert kwargs["url"] == f"{rest_address}{request_url_path}"
        assert kwargs["json"] == request_json

    @patch("requests.session", spec=Session)
    @patch("cosmpy.common.rest_client.MessageToDict")
    def test_post_error(self, messageToDict_mock, session_mock):
        """
        Test post method for the negative result.

        :param messageToDict_mock: mock
        :param session_mock: mock
        """

        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 400
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json

        session_mock.return_value.post.return_value = resp

        with self.assertRaises(Exception) as context:
            client.post(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)
        self.assertTrue("Error when sending a POST request" in str(context.exception))

    @staticmethod
    @patch("requests.session", spec=Session)
    def test_session_close_on_object_deletion(session_mock):
        """
        Test session close for the positive result.

        :param session_mock: mock
        """

        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        del client
        session_mock.return_value.close.assert_called_once_with()
