import requests


class RestClient:
    def __init__(self, rest_address: str):
        self._session = requests.session()
        self.rest_address = rest_address

    def query(self, request: str) -> bytes:
        response = self._session.get(url=self.rest_address + request)
        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a query request.\n Request: {request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    def post(self, url_path, json_request: dict) -> bytes:
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = self._session.post(
            url=self.rest_address + url_path,
            json=json_request,
            headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error when sending a query request.\n Request: {json_request}\n Response: {response.status_code}, {str(response.content)})"
            )
        return response.content

    def __del__(self):
        self._session.close()
