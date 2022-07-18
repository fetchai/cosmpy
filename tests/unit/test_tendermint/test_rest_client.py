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
"""Tests for REST implementation of Cosmos Base Tendermint."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import Int32Value  # noqa # needed for protobuf decode

from cosmpy.common.utils import json_encode
from cosmpy.protos.cosmos.base.tendermint.v1beta1.query_pb2 import (
    GetBlockByHeightRequest,
    GetBlockByHeightResponse,
    GetLatestBlockRequest,
    GetLatestBlockResponse,
    GetLatestValidatorSetRequest,
    GetLatestValidatorSetResponse,
    GetNodeInfoRequest,
    GetNodeInfoResponse,
    GetSyncingRequest,
    GetSyncingResponse,
    GetValidatorSetByHeightRequest,
    GetValidatorSetByHeightResponse,
)
from cosmpy.tendermint.rest_client import CosmosBaseTendermintRestClient
from tests.helpers import MockRestClient

TYPE = {
    "@type": "type.googleapis.com/google.protobuf.Int32Value",
    "value": "42",
}


class CosmosBaseTendermintRestClientTestCase(TestCase):
    """Test case for CosmosBaseTendermintRestClient class."""

    REST_CLIENT = CosmosBaseTendermintRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, CosmosBaseTendermintRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_GetNodeInfo(self):
        """Test GetNodeInfo method."""
        content = {
            "default_node_info": {
                "protocol_version": {
                    "p2p": "12",
                    "block": "12",
                    "app": "12",
                },
                "default_node_id": "string",
                "listen_addr": "string",
                "network": "string",
                "version": "string",
                "channels": "string",
                "moniker": "string",
                "other": {"tx_index": "string", "rpc_address": "string"},
            },
            "application_version": {
                "name": "string",
                "app_name": "string",
                "version": "string",
                "git_commit": "string",
                "build_tags": "string",
                "go_version": "string",
                "build_deps": [{"path": "string", "version": "string", "sum": "12"}],
            },
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetNodeInfoResponse())

        assert rest_client.GetNodeInfo(GetNodeInfoRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/base/tendermint/v1beta1/node_info"

    def test_GetSyncing(self):
        """Test GetSyncing method."""
        content = {"syncing": True}
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetSyncingResponse())

        assert rest_client.GetSyncing(GetSyncingRequest()) == expected_response
        assert mock_client.last_base_url == "/cosmos/base/tendermint/v1beta1/syncing"

    def test_GetLatestBlock(self):
        """Test GetLatestBlock method."""
        content = {
            "block_id": {
                "hash": "string",
                "part_set_header": {"total": 0, "hash": "string"},
            },
            "block": {
                "header": {
                    "version": {"block": "12", "app": "12"},
                    "chain_id": "string",
                    "height": "12",
                    "time": "2022-03-29T10:21:54.568Z",
                    "last_block_id": {
                        "hash": "string",
                        "part_set_header": {"total": 0, "hash": "string"},
                    },
                    "last_commit_hash": "string",
                    "data_hash": "string",
                    "validators_hash": "string",
                    "next_validators_hash": "string",
                    "consensus_hash": "string",
                    "app_hash": "string",
                    "last_results_hash": "string",
                    "evidence_hash": "string",
                    "proposer_address": "string",
                },
                "data": {"txs": ["string"]},
                "evidence": {"evidence": []},
                "last_commit": {
                    "height": "12",
                    "round": 0,
                    "block_id": {
                        "hash": "string",
                        "part_set_header": {"total": 0, "hash": "string"},
                    },
                    "signatures": [
                        {
                            "block_id_flag": "BLOCK_ID_FLAG_UNKNOWN",
                            "validator_address": "string",
                            "timestamp": "2022-03-29T10:21:54.569Z",
                            "signature": "string",
                        }
                    ],
                },
            },
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetLatestBlockResponse())

        assert rest_client.GetLatestBlock(GetLatestBlockRequest()) == expected_response
        assert (
            mock_client.last_base_url == "/cosmos/base/tendermint/v1beta1/blocks/latest"
        )

    def test_GetBlockByHeight(self):
        """Test GetBlockByHeight method."""
        content = {
            "block_id": {
                "hash": "string",
                "part_set_header": {"total": 0, "hash": "string"},
            },
            "block": {
                "header": {
                    "version": {"block": "12", "app": "12"},
                    "chain_id": "string",
                    "height": "12",
                    "time": "2022-03-29T10:27:01.686Z",
                    "last_block_id": {
                        "hash": "string",
                        "part_set_header": {"total": 0, "hash": "string"},
                    },
                    "last_commit_hash": "string",
                    "data_hash": "string",
                    "validators_hash": "string",
                    "next_validators_hash": "string",
                    "consensus_hash": "string",
                    "app_hash": "string",
                    "last_results_hash": "string",
                    "evidence_hash": "string",
                    "proposer_address": "string",
                },
                "data": {"txs": ["string"]},
                "evidence": {"evidence": []},
                "last_commit": {
                    "height": "12",
                    "round": 0,
                    "block_id": {
                        "hash": "string",
                        "part_set_header": {"total": 0, "hash": "string"},
                    },
                    "signatures": [
                        {
                            "block_id_flag": "BLOCK_ID_FLAG_UNKNOWN",
                            "validator_address": "string",
                            "timestamp": "2022-03-29T10:27:01.687Z",
                            "signature": "string",
                        }
                    ],
                },
            },
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetBlockByHeightResponse())

        assert (
            rest_client.GetBlockByHeight(GetBlockByHeightRequest(height=123))
            == expected_response
        )
        assert mock_client.last_base_url == "/cosmos/base/tendermint/v1beta1/blocks/123"

    def test_GetLatestValidatorSet(self):
        """Test GetLatestValidatorSet method."""
        content = {
            "block_height": "12",
            "validators": [
                {
                    "address": "string",
                    "pub_key": TYPE,
                    "voting_power": "12",
                    "proposer_priority": "12",
                }
            ],
            "pagination": {"next_key": "string", "total": "12"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetLatestValidatorSetResponse())

        assert (
            rest_client.GetLatestValidatorSet(GetLatestValidatorSetRequest())
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/base/tendermint/v1beta1/validatorsets/latest"
        )

    def test_GetValidatorSetByHeight(self):
        """Test GetValidatorSetByHeight method."""
        content = {
            "block_height": "12",
            "validators": [
                {
                    "address": "string",
                    "pub_key": TYPE,
                    "voting_power": "12",
                    "proposer_priority": "12",
                }
            ],
            "pagination": {"next_key": "string", "total": "12"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, GetValidatorSetByHeightResponse())

        assert (
            rest_client.GetValidatorSetByHeight(
                GetValidatorSetByHeightRequest(height=123)
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/cosmos/base/tendermint/v1beta1/validatorsets/123"
        )
