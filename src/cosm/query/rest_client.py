import urllib.error
import urllib.request


class QueryRestClient:
    def __init__(self, rest_address: str):
        self.rest_address = rest_address

    def query(self, request: str) -> str:
        url = self.rest_address + request

        try:
            with urllib.request.urlopen(url) as f:
                response = f.read().decode("utf-8")
                return response
        except urllib.error.HTTPError as e:
            raise RuntimeError(
                f"Error when sending a query request.\n Request: {request}\n Response: {e.code}, {str(e.read().decode('utf-8'))})"
            )
