"""Rest Queries."""

import requests


class QueryRestClient:
    """Query REST client."""

    def __init__(self, rest_address: str) -> None:
        """
        Create a REST query

        :param rest_address: the address the REST client must communicate with
        :return: None
        """
        self._session = requests.session()
        self.rest_address = rest_address

    def get(self, request: str) -> bytes:
        """
        Send a GET request

        :param request: the URL path after the default rest address
        :return: response's content
        """
        response = self._session.get(url=self.rest_address + request)
        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a query request.\n Request: {request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    def post(self, url_path, json_request: dict) -> bytes:
        """
        Send a POST request

        :param url_path: the URL path after the default rest address
        :param json_request: the json data

        :return: response's content
        """
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = self._session.post(
            url=self.rest_address + url_path, json=json_request, headers=headers
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a query request.\n Request: {json_request}\n Response: {response.status_code}, {str(response.content)})"
            )

        return response.content

    def __del__(self):
        self._session.close()
