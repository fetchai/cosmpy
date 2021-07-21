import requests
from urllib.parse import urlencode
from google.protobuf.descriptor import Descriptor
from google.protobuf.json_format import MessageToDict


class RestClient:
    def __init__(self, rest_address: str):
        self._session = requests.session()
        self.rest_address = rest_address

    def get(self, url_base_path: str, request: Descriptor) -> bytes:
        json_request = MessageToDict(request)
        url_encoded_request = urlencode(json_request)
        response = self._session.get(
            url=f"{self.rest_address}{url_base_path}&{url_encoded_request}"
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a GET request.\n Request: {request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    def post(self, url_base_path: str, request: Descriptor) -> bytes:
        json_request = MessageToDict(request)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = self._session.post(
            url=f"{self.rest_address}{url_base_path}",
            json=json_request,
            headers=headers,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a POST request.\n Request: {json_request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    def __del__(self):
        self._session.close()
