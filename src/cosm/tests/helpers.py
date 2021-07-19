"""Helpers methods and classes for testing."""

from unittest.mock import Mock


class MockResponse(Mock):
    """Mock Response."""

    def __init__(self, status_code: int, content: str):
        """Initialize."""
        super().__init__()
        self.status_code = status_code
        self.content = content


class MockSession(Mock):
    """Mock Session."""

    def __init__(self, status_code: int, content: str):
        """Initialize."""
        super().__init__()
        self.status_code = status_code
        self.content = content
        self.last_url = ""

    def get(self, url: str) -> MockResponse:
        """Handle GET request."""
        self.last_url = url
        return MockResponse(self.status_code, self.content)
