import pytest
from .urls import ParsedUrl, Protocol, parse_url


@pytest.mark.parametrize("input_url,parse_result", [
    ("grpc+https://foo.bar.baz", ParsedUrl(hostname='foo.bar.baz', port=443, secure=True, protocol=Protocol.GRPC)),
    ("grpc+https://foo.bar.baz:8000", ParsedUrl(hostname='foo.bar.baz', port=8000, secure=True, protocol=Protocol.GRPC)),
    ("grpc+http://foo.bar.baz", ParsedUrl(hostname='foo.bar.baz', port=80, secure=False, protocol=Protocol.GRPC)),
    ("grpc+http://foo.bar.baz:8000", ParsedUrl(hostname='foo.bar.baz', port=8000, secure=False, protocol=Protocol.GRPC)),
    ("rest+https://foo.bar.baz", ParsedUrl(hostname='foo.bar.baz', port=443, secure=True, protocol=Protocol.REST)),
    ("rest+https://foo.bar.baz:8000", ParsedUrl(hostname='foo.bar.baz', port=8000, secure=True, protocol=Protocol.REST)),
    ("rest+http://foo.bar.baz", ParsedUrl(hostname='foo.bar.baz', port=80, secure=False, protocol=Protocol.REST)),
    ("rest+http://foo.bar.baz:8000", ParsedUrl(hostname='foo.bar.baz', port=8000, secure=False, protocol=Protocol.REST)),

])
def test_parsing_urls(input_url, parse_result):
    assert parse_url(input_url) == parse_result
