"""Helpers methods and classes for testing."""


class MockQueryRestClient:
    """Mock QueryRestClient"""

    def __init__(self, content: str):
        """Initialize."""
        self.content = content
        self.last_request = ""

    def get(self, request: str) -> str:
        """Handle GET request."""
        self.last_request = request
        return self.content

    def close(self):
        ...
