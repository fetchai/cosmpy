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
"""Tests for REST implementation of IBC Core Channel."""
from typing import Dict, Tuple
from unittest import TestCase

from google.protobuf.json_format import ParseDict
from google.protobuf.wrappers_pb2 import Int32Value  # noqa # needed for protobuf decode

from cosmpy.common.utils import json_encode
from cosmpy.ibc.core.channel.rest_client import IBCCoreChannelRestClient  # type: ignore
from cosmpy.protos.ibc.core.channel.v1.query_pb2 import (
    QueryChannelClientStateRequest,
    QueryChannelClientStateResponse,
    QueryChannelConsensusStateRequest,
    QueryChannelConsensusStateResponse,
    QueryChannelRequest,
    QueryChannelResponse,
    QueryChannelsRequest,
    QueryChannelsResponse,
    QueryConnectionChannelsRequest,
    QueryConnectionChannelsResponse,
    QueryNextSequenceReceiveRequest,
    QueryNextSequenceReceiveResponse,
    QueryPacketAcknowledgementRequest,
    QueryPacketAcknowledgementResponse,
    QueryPacketAcknowledgementsRequest,
    QueryPacketAcknowledgementsResponse,
    QueryPacketCommitmentRequest,
    QueryPacketCommitmentResponse,
    QueryPacketCommitmentsRequest,
    QueryPacketCommitmentsResponse,
    QueryPacketReceiptRequest,
    QueryPacketReceiptResponse,
    QueryUnreceivedAcksRequest,
    QueryUnreceivedAcksResponse,
    QueryUnreceivedPacketsRequest,
    QueryUnreceivedPacketsResponse,
)
from tests.helpers import MockRestClient

TYPE = {
    "@type": "type.googleapis.com/google.protobuf.Int32Value",
    "value": "42",
}


class IBCCoreChannelRestClientTestCase(TestCase):
    """Test case for IBCCoreChannelRestClient class."""

    REST_CLIENT = IBCCoreChannelRestClient

    def make_clients(
        self, response_content: Dict
    ) -> Tuple[MockRestClient, IBCCoreChannelRestClient]:
        """
        Make  mock client and rest client api for specific content.

        :param response_content: dict
        :return: rest client instance
        """
        mock_client = MockRestClient(json_encode(response_content).encode("utf-8"))
        rest_client = self.REST_CLIENT(mock_client)
        return mock_client, rest_client

    def test_Channel(self):
        """Test Channel method."""
        content = {
            "channel": {
                "state": "STATE_UNINITIALIZED_UNSPECIFIED",
                "ordering": "ORDER_NONE_UNSPECIFIED",
                "counterparty": {"port_id": "1", "channel_id": "1"},
                "connection_hops": ["1"],
                "version": "1",
            },
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryChannelResponse())

        assert (
            rest_client.Channel(
                QueryChannelRequest(channel_id="channel_id", port_id="port_id")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/channel_id/ports/port_id"
        )

    def test_Channels(self):
        """Test Channels method."""
        content = {
            "channels": [
                {
                    "state": "STATE_UNINITIALIZED_UNSPECIFIED",
                    "ordering": "ORDER_NONE_UNSPECIFIED",
                    "counterparty": {"port_id": "1", "channel_id": "1"},
                    "connection_hops": ["1"],
                    "version": "1",
                    "port_id": "1",
                    "channel_id": "1",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryChannelsResponse())

        assert rest_client.Channels(QueryChannelsRequest()) == expected_response
        assert mock_client.last_base_url == "/ibc/core/channel/v1beta1/channels"

    def test_ConnectionChannels(self):
        """Test ConnectionChannels method."""
        content = {
            "channels": [
                {
                    "state": "STATE_UNINITIALIZED_UNSPECIFIED",
                    "ordering": "ORDER_NONE_UNSPECIFIED",
                    "counterparty": {"port_id": "1", "channel_id": "1"},
                    "connection_hops": ["1"],
                    "version": "1",
                    "port_id": "1",
                    "channel_id": "1",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryConnectionChannelsResponse())

        assert (
            rest_client.ConnectionChannels(
                QueryConnectionChannelsRequest(connection="connection")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/connections/connection/channels"
        )

    def test_ChannelClientState(self):
        """Test ChannelClientState method."""
        content = {
            "identified_client_state": {"client_id": "1", "client_state": TYPE},
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryChannelClientStateResponse())

        assert (
            rest_client.ChannelClientState(
                QueryChannelClientStateRequest(channel_id="1", port_id="1")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/client_state"
        )

    def test_ChannelConsensusState(self):
        """Test ChannelConsensusState method."""
        content = {
            "consensus_state": TYPE,
            "client_id": "1",
            "proof": "string",
            "proof_height": {
                "revision_number": "1",
            },
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryChannelConsensusStateResponse())

        assert (
            rest_client.ChannelConsensusState(
                QueryChannelConsensusStateRequest(
                    channel_id="1", port_id="1", revision_number=1, revision_height=1
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/consensus_state/revision/1/height/1"
        )

    def test_PacketCommitment(self):
        """Test PacketCommitment method."""
        content = {
            "commitment": "string",
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryPacketCommitmentResponse())

        assert (
            rest_client.PacketCommitment(
                QueryPacketCommitmentRequest(sequence=1, channel_id="1", port_id="1")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_commitments/1"
        )

    def test_PacketCommitments(self):
        """Test PacketCommitments method."""
        content = {
            "commitments": [
                {
                    "port_id": "1",
                    "channel_id": "1",
                    "sequence": "1",
                    "data": "string",
                }
            ],
            "pagination": {"next_key": "string", "total": "1"},
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryPacketCommitmentsResponse())

        assert (
            rest_client.PacketCommitments(
                QueryPacketCommitmentsRequest(channel_id="1", port_id="1")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_commitments"
        )

    def test_PacketReceipt(self):
        """Test PacketReceipt method."""
        content = {
            "received": True,
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryPacketReceiptResponse())

        assert (
            rest_client.PacketReceipt(
                QueryPacketReceiptRequest(channel_id="1", port_id="1", sequence=1)
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_receipts/1"
        )

    def test_PacketAcknowledgement(self):
        """Test PacketAcknowledgement method."""
        content = {
            "acknowledgement": "string",
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryPacketAcknowledgementResponse())

        assert (
            rest_client.PacketAcknowledgement(
                QueryPacketAcknowledgementRequest(
                    port_id="1", channel_id="1", sequence=1
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_acks/1"
        )

    def test_PacketAcknowledgements(self):
        """Test PacketAcknowledgements method."""
        content = {
            "acknowledgements": [
                {"port_id": "1", "channel_id": "1", "sequence": "1", "data": "string"}
            ],
            "pagination": {"next_key": "string", "total": "1"},
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryPacketAcknowledgementsResponse())

        assert (
            rest_client.PacketAcknowledgements(
                QueryPacketAcknowledgementsRequest(channel_id="1", port_id="1")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_acknowledgements"
        )

    def test_UnreceivedPackets(self):
        """Test UnreceivedPackets method."""
        content = {
            "sequences": ["1"],
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryUnreceivedPacketsResponse())

        assert (
            rest_client.UnreceivedPackets(
                QueryUnreceivedPacketsRequest(
                    channel_id="1", port_id="1", packet_commitment_sequences=[1]
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_commitments/1/unreceived_packets"
        )

    def test_UnreceivedAcks(self):
        """Test UnreceivedAcks method."""
        content = {
            "sequences": ["1"],
            "height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryUnreceivedAcksResponse())

        assert (
            rest_client.UnreceivedAcks(
                QueryUnreceivedAcksRequest(
                    packet_ack_sequences=[1], channel_id="1", port_id="1"
                )
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/packet_commitments/1/unreceived_acks"
        )

    def test_NextSequenceReceive(self):
        """Test NextSequenceReceive method."""
        content = {
            "next_sequence_receive": "1",
            "proof": "string",
            "proof_height": {"revision_number": "1", "revision_height": "1"},
        }
        mock_client, rest_client = self.make_clients(content)
        expected_response = ParseDict(content, QueryNextSequenceReceiveResponse())

        assert (
            rest_client.NextSequenceReceive(
                QueryNextSequenceReceiveRequest(port_id="1", channel_id="1")
            )
            == expected_response
        )
        assert (
            mock_client.last_base_url
            == "/ibc/core/channel/v1beta1/channels/1/ports/1/next_sequence"
        )
