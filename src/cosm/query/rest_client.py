import requests


class QueryRestClient:
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
