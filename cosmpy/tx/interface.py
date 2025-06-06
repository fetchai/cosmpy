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

"""Interface for the Tx functionality of CosmosSDK."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import cosmpy.protos.cosmos.tx.v1beta1.service_pb2 as svc


class TxInterface(ABC):
    """Tx abstract class."""

    @abstractmethod
    def Simulate(
        self,
        request: svc.SimulateRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> svc.SimulateResponse:
        """
        Simulate executing a transaction to estimate gas usage.

        :param request: SimulateRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: SimulateResponse
        """

    @abstractmethod
    def GetTx(
        self,
        request: svc.GetTxRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> svc.GetTxResponse:
        """
        GetTx fetches a tx by hash.

        :param request: GetTxRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: GetTxResponse
        """

    @abstractmethod
    def BroadcastTx(
        self,
        request: svc.BroadcastTxRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> svc.BroadcastTxResponse:
        """
        BroadcastTx broadcast transaction.

        :param request: BroadcastTxRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: BroadcastTxResponse
        """

    @abstractmethod
    def GetTxsEvent(
        self,
        request: svc.GetTxsEventRequest,
        metadata: Optional[Tuple[Tuple[str, str]]] = None,
    ) -> svc.GetTxsEventResponse:
        """
        GetTxsEvent fetches txs by event.

        :param request: GetTxsEventRequest
        :param metadata: The metadata for the call or None. metadata are additional headers
        :return: GetTxsEventResponse
        """
