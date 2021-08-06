from typing import List, Optional
from urllib.parse import urlencode

import requests
from google.protobuf.descriptor import Descriptor
from google.protobuf.json_format import MessageToDict


class RestClient:
    def __init__(self, rest_address: str):
        self._session = requests.session()
        self.rest_address = rest_address

    def get(
        self,
        url_base_path: str,
        request: Descriptor,
        used_params: Optional[List[str]] = None,
    ) -> bytes:

        json_request = MessageToDict(request)

        # Remove params that are already in url_base_path
        if used_params is not None:
            for param in used_params:
                json_request.pop(param)

        url_encoded_request = urlencode(json_request)
        response = self._session.get(
            url=f"{self.rest_address}{url_base_path}?{url_encoded_request}"
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a GET request.\n Request: {json_request}\n Response: {response.status_code}, {str(response.content)})"
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
