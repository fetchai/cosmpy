# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
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
"""Tests for REST implementation of Evidence."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import (  # noqa  # needed for protobuf decode
    Int32Value,
)

from cosmpy.common.utils import json_encode
from cosmpy.evidence.rest_client import EvidenceRestClient
from cosmpy.protos.cosmos.evidence.v1beta1.query_pb2 import (
    QueryAllEvidenceRequest,
    QueryAllEvidenceResponse,
    QueryEvidenceRequest,
    QueryEvidenceResponse,
)
from tests.helpers import MockRestClient


class EvidenceRestClientTestCase(TestCase):
    """Test case for EvidenceRestClient class."""

    REST_CLIENT = EvidenceRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, EvidenceRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_Evidence(self):
        """Test Evidence method."""
        content = {
            "evidence": {
                "@type": "type.googleapis.com/google.protobuf.Int32Value",
                "value": "42",
            }
        }
        mock_client, evidence = self.make_clients(content)
        expected_response = ParseDict(content, QueryEvidenceResponse())

        assert (
            evidence.Evidence(QueryEvidenceRequest(evidence_hash=b"hash"))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/evidence/v1beta1/evidence/b'hash'"

    def test_AllEvidence(self):
        """Test AllEvidence method."""
        content = {
            "evidence": [
                {
                    "@type": "type.googleapis.com/google.protobuf.Int32Value",
                    "value": "42",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, evidence = self.make_clients(content)
        expected_response = ParseDict(content, QueryAllEvidenceResponse())

        assert evidence.AllEvidence(QueryAllEvidenceRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/evidence/v1beta1/evidence"
