# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

import pytest

from cosmpy.aerial.urls import ParsedUrl, Protocol, parse_url


@pytest.mark.parametrize(
    "input_url,parse_result",
    [
        (
            "grpc+https://foo.bar.baz",
            ParsedUrl(
                hostname="foo.bar.baz", port=443, secure=True, protocol=Protocol.GRPC
            ),
        ),
        (
            "grpc+https://foo.bar.baz:8000",
            ParsedUrl(
                hostname="foo.bar.baz", port=8000, secure=True, protocol=Protocol.GRPC
            ),
        ),
        (
            "grpc+http://foo.bar.baz",
            ParsedUrl(
                hostname="foo.bar.baz", port=80, secure=False, protocol=Protocol.GRPC
            ),
        ),
        (
            "grpc+http://foo.bar.baz:8000",
            ParsedUrl(
                hostname="foo.bar.baz", port=8000, secure=False, protocol=Protocol.GRPC
            ),
        ),
        (
            "rest+https://foo.bar.baz",
            ParsedUrl(
                hostname="foo.bar.baz", port=443, secure=True, protocol=Protocol.REST
            ),
        ),
        (
            "rest+https://foo.bar.baz:8000",
            ParsedUrl(
                hostname="foo.bar.baz", port=8000, secure=True, protocol=Protocol.REST
            ),
        ),
        (
            "rest+http://foo.bar.baz",
            ParsedUrl(
                hostname="foo.bar.baz", port=80, secure=False, protocol=Protocol.REST
            ),
        ),
        (
            "rest+http://foo.bar.baz:8000",
            ParsedUrl(
                hostname="foo.bar.baz", port=8000, secure=False, protocol=Protocol.REST
            ),
        ),
    ],
)
def test_parsing_urls(input_url, parse_result):
    assert parse_url(input_url) == parse_result
