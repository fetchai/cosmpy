import requests


class RestClient:
    def __init__(self, rest_address: str):
        self._session = requests.session()
        self.rest_address = rest_address

    def query(self, request: str):
        response = self._session.get(url=self.rest_address + request)
        if response.status_code != 200:
            raise RuntimeError(response)
        return response.json()
