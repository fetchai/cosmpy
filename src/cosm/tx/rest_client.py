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

"""Implementation of Tx interface using REST."""

from google.protobuf.json_format import Parse

from cosm.common.rest_client import RestClient
from cosm.tx.interface import TxInterface
from cosmos.tx.v1beta1.service_pb2 import (
    BroadcastTxRequest,
    BroadcastTxResponse,
    GetTxRequest,
    GetTxResponse,
    GetTxsEventRequest,
    GetTxsEventResponse,
    SimulateRequest,
    SimulateResponse,
)


class TxRestClient(TxInterface):
    """Tx REST client."""

    txs_url_path = "/cosmos/tx/v1beta1/txs"

    def __init__(self, rest_client: RestClient) -> None:
        """
        Create a Tx rest client

        :param rest_client: RestClient api
        """
        self.rest_client = rest_client

    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        """Simulate simulates executing a transaction for estimating gas usage."""
        response = self.rest_client.post("/cosmos/tx/v1beta1/simulate", request)
        return Parse(response, SimulateResponse())

    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        """GetTx fetches a tx by hash."""
        response = self.rest_client.get(self.txs_url_path, request)
        return Parse(response, GetTxResponse())

    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        """BroadcastTx broadcast transaction."""
        response = self.rest_client.post(self.txs_url_path, request)
        return Parse(response, BroadcastTxResponse())

    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        """GetTxsEvent fetches txs by event."""
        response = self.rest_client.get(self.txs_url_path, request)
        return Parse(response, GetTxsEventResponse())
