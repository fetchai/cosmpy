import pytest


def pytest_collection_modifyitems(_, items):
    # Remove third party tests from integration tests
    for item in items:
        if "third_party" in item.nodeid:
            if "integration" in item.keywords:
                item.add_marker(pytest.mark.skip(reason="Skipped in integration tests"))
