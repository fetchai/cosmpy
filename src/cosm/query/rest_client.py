import urllib.error
from urllib.request import Request, urlopen


class QueryRestClient:
    def __init__(self, rest_address: str):
        self.rest_address = rest_address

    def get(self, request: str) -> str:
        url = self.rest_address + request

        try:
            with urllib.request.urlopen(url) as f:
                response = f.read().decode("utf-8")
                return response
        except urllib.error.HTTPError as e:
            raise RuntimeError(
                f"HTTPError when sending a get request.\n Request: {request}\n Response: {e.code}, {str(e.read().decode('utf-8'))})"
            )
        except urllib.error.URLError as e:
            raise RuntimeError(
                f"URLError when sending a get request.\n Request: {request}, Exception: {e})"
            )
        except Exception as e:
            raise RuntimeError(
                f"Exception during sending a get request.\n Request: {request}, Exception: {e})"
            )

    def post(self, url_path, json_request: dict) -> str:
        try:
            req = Request(self.rest_address + url_path)
            req.add_header("Content-type", "application/json")
            req.add_header("Accept", "application/json")
            response = (
                urlopen(req, data=str(json_request).encode("utf-8"))
                .read()
                .decode("utf-8")
            )
            return response
        except urllib.error.HTTPError as e:
            raise RuntimeError(
                f"HTTPError when sending a get request.\n Request: {url_path}, with json data: {json_request}\n Response: {e.code}, {str(e.read().decode('utf-8'))})"
            )
        except urllib.error.URLError as e:
            raise RuntimeError(
                f"URLError when sending a get request.\n Request: {url_path}, with json data: {json_request}, Exception: {e})"
            )
        except Exception as e:
            raise RuntimeError(
                f"Exception during sending a get request.\n Request: {url_path}, with json data: {json_request}, Exception: {e})"
            )
