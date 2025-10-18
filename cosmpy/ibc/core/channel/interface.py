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
"""Interface for the IBC Core Channel functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

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


class IBCCoreChannel(ABC):
    """IBC Core Channel abstract class."""

    @abstractmethod
    def Channel(
        self,
        request: QueryChannelRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryChannelResponse:
        """
        Channel queries an IBC Channel.

        :param request: QueryChannelRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryChannelResponse
        """

    @abstractmethod
    def Channels(
        self,
        request: QueryChannelsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryChannelsResponse:
        """
        Channels queries all the IBC channels of a chain.

        :param request: QueryChannelsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryChannelsResponse
        """

    @abstractmethod
    def ConnectionChannels(
        self,
        request: QueryConnectionChannelsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryConnectionChannelsResponse:
        """
        ConnectionChannels queries all the channels associated with a connection.

        :param request: QueryConnectionChannelsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryConnectionChannelsResponse
        """

    @abstractmethod
    def ChannelClientState(
        self,
        request: QueryChannelClientStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryChannelClientStateResponse:
        """
        ChannelClientState queries for the client state for the channel associated with the provided channel identifiers.

        :param request: QueryChannelClientStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryChannelClientStateResponse
        """

    @abstractmethod
    def ChannelConsensusState(
        self,
        request: QueryChannelConsensusStateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryChannelConsensusStateResponse:
        """
        ChannelConsensusState queries for the consensus state for the channel associated with the provided channel identifiers.

        :param request: QueryChannelConsensusStateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryChannelConsensusStateResponse
        """

    @abstractmethod
    def PacketCommitment(
        self,
        request: QueryPacketCommitmentRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPacketCommitmentResponse:
        """
        PacketCommitment queries a stored packet commitment hash.

        :param request: QueryPacketCommitmentRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryPacketCommitmentResponse
        """

    @abstractmethod
    def PacketCommitments(
        self,
        request: QueryPacketCommitmentsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPacketCommitmentsResponse:
        """
        PacketCommitments returns all the packet commitments hashes associated with a channel.

        :param request: QueryPacketCommitmentsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryPacketCommitmentsResponse
        """

    @abstractmethod
    def PacketReceipt(
        self,
        request: QueryPacketReceiptRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPacketReceiptResponse:
        """
        PacketReceipt queries if a given packet sequence has been received on the queried chain.

        :param request: QueryPacketReceiptRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryPacketReceiptResponse
        """

    @abstractmethod
    def PacketAcknowledgement(
        self,
        request: QueryPacketAcknowledgementRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPacketAcknowledgementResponse:
        """
        PacketAcknowledgement queries a stored packet acknowledgment hash.

        :param request: QueryPacketAcknowledgementRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryPacketAcknowledgementResponse
        """

    @abstractmethod
    def PacketAcknowledgements(
        self,
        request: QueryPacketAcknowledgementsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryPacketAcknowledgementsResponse:
        """
        PacketAcknowledgements returns all the packet acknowledgments associated with a channel.

        :param request: QueryPacketAcknowledgementsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryPacketAcknowledgementsResponse
        """

    @abstractmethod
    def UnreceivedPackets(
        self,
        request: QueryUnreceivedPacketsRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryUnreceivedPacketsResponse:
        """
        UnreceivedPackets returns all the unreceived IBC packets associated with a channel and sequences.

        :param request: QueryUnreceivedPacketsRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryUnreceivedPacketsResponse
        """

    @abstractmethod
    def UnreceivedAcks(
        self,
        request: QueryUnreceivedAcksRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryUnreceivedAcksResponse:
        """
        UnreceivedAcks returns all the unreceived IBC acknowledgments associated with a channel and sequences.

        :param request: QueryUnreceivedAcksRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryUnreceivedAcksResponse
        """

    @abstractmethod
    def NextSequenceReceive(
        self,
        request: QueryNextSequenceReceiveRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> QueryNextSequenceReceiveResponse:
        """
        NextSequenceReceive returns the next receive sequence for a given channel.

        :param request: QueryNextSequenceReceiveRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: QueryNextSequenceReceiveResponse
        """
