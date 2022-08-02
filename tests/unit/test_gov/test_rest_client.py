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
"""Tests for REST implementation of Gov."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict

from cosmpy.common.utils import json_encode
from cosmpy.gov.rest_client import GovRestClient
from cosmpy.protos.cosmos.gov.v1beta1.query_pb2 import (
    QueryDepositRequest,
    QueryDepositResponse,
    QueryDepositsRequest,
    QueryDepositsResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryProposalRequest,
    QueryProposalResponse,
    QueryProposalsRequest,
    QueryProposalsResponse,
    QueryTallyResultRequest,
    QueryTallyResultResponse,
    QueryVoteRequest,
    QueryVoteResponse,
    QueryVotesRequest,
    QueryVotesResponse,
)
from tests.helpers import MockRestClient


class GovRestClientTestCase(TestCase):
    """Test case for GovRestClient class."""

    REST_CLIENT = GovRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, GovRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_Proposal(self):
        """Test Proposal method."""
        content = {
            "proposal": {
                "proposal_id": "10",
                "status": "PROPOSAL_STATUS_UNSPECIFIED",
                "final_tally_result": {
                    "yes": "string",
                    "abstain": "string",
                    "no": "string",
                    "no_with_veto": "string",
                },
                "submit_time": "2022-02-21T13:03:00.840Z",
                "deposit_end_time": "2022-02-21T13:03:00.840Z",
                "total_deposit": [{"denom": "string", "amount": "string"}],
                "voting_start_time": "2022-02-21T13:03:00.840Z",
                "voting_end_time": "2022-02-21T13:03:00.840Z",
            }
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryProposalResponse())

        assert gov.Proposal(QueryProposalRequest(proposal_id=1)) == expected_response
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/1"

    def test_Proposals(self):
        """Test Proposals method."""
        content = {
            "proposals": [
                {
                    "proposal_id": "10",
                    "status": "PROPOSAL_STATUS_UNSPECIFIED",
                    "final_tally_result": {
                        "yes": "string",
                        "abstain": "string",
                        "no": "string",
                        "no_with_veto": "string",
                    },
                    "submit_time": "2022-02-21T13:09:02.841Z",
                    "deposit_end_time": "2022-02-21T13:09:02.842Z",
                    "total_deposit": [{"denom": "string", "amount": "string"}],
                    "voting_start_time": "2022-02-21T13:09:02.842Z",
                    "voting_end_time": "2022-02-21T13:09:02.842Z",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryProposalsResponse())

        assert gov.Proposals(QueryProposalsRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/"

    def test_Vote(self):
        """Test Vote method."""
        content = {"vote": {"proposal_id": "10", "voter": "addr"}}
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryVoteResponse())

        assert (
            gov.Vote(QueryVoteRequest(proposal_id=10, voter="addr"))
            == expected_response
        )
        assert (
            mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/10/votes/addr"
        )

    def test_Votes(self):
        """Test Votes method."""
        content = {
            "votes": [{"proposal_id": "1", "voter": "string"}],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryVotesResponse())

        assert gov.Votes(QueryVotesRequest(proposal_id=1)) == expected_response
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/1/votes/"

    def test_Params(self):
        """Test Params method."""
        content = {
            "voting_params": {"voting_period": "10s"},
            "deposit_params": {
                "min_deposit": [{"denom": "string", "amount": "string"}],
                "max_deposit_period": "10s",
            },
            "tally_params": {
                "quorum": "string",
                "threshold": "string",
                "veto_threshold": "string",
            },
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryParamsResponse())

        assert gov.Params(QueryParamsRequest(params_type="some")) == expected_response
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/params/some"

    def test_Deposit(self):
        """Test Deposit method."""
        content = {
            "deposit": {
                "proposal_id": "10",
                "depositor": "string",
                "amount": [{"denom": "string", "amount": "10"}],
            }
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryDepositResponse())

        assert (
            gov.Deposit(QueryDepositRequest(proposal_id=10, depositor="depositor"))
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/gov/v1beta1/proposals/10/deposits/depositor"
        )

    def test_Deposits(self):
        """Test Deposits method."""
        content = {
            "deposits": [
                {
                    "proposal_id": "10",
                    "depositor": "string",
                    "amount": [{"denom": "string", "amount": "10"}],
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryDepositsResponse())

        assert gov.Deposits(QueryDepositsRequest(proposal_id=1)) == expected_response
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/1/deposits/"

    def test_TallyResult(self):
        """Test TallyResult method."""
        content = {
            "tally": {
                "yes": "string",
                "abstain": "string",
                "no": "string",
                "no_with_veto": "string",
            }
        }
        mock_client, gov = self.make_clients(content)
        expected_response = ParseDict(content, QueryTallyResultResponse())

        assert (
            gov.TallyResult(QueryTallyResultRequest(proposal_id=10))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/gov/v1beta1/proposals/10/tally"
