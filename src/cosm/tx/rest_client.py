"""Implementation of Tx interface using REST."""

from urllib.parse import urlencode

from google.protobuf.json_format import MessageToDict, Parse

from cosm.query.rest_client import QueryRestClient as RestClient
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

        :param rest_client: QueryRestClient api
        """
        self.rest_client = rest_client

    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        """Simulate simulates executing a transaction for estimating gas usage."""
        json_request = MessageToDict(request)
        response = self.rest_client.post("/cosmos/tx/v1beta1/simulate", json_request)
        return Parse(response, SimulateResponse())

    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        """GetTx fetches a tx by hash."""
        json_request = MessageToDict(request)
        url_encoded_request = urlencode(json_request)
        response = self.rest_client.get(
            f"{self.txs_url_path}&{url_encoded_request}",
        )
        return Parse(response, GetTxResponse())

    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        """BroadcastTx broadcast transaction."""
        json_request = MessageToDict(request)
        response = self.rest_client.post(self.txs_url_path, json_request)
        return Parse(response, BroadcastTxResponse())

    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        """GetTxsEvent fetches txs by event."""
        json_request = MessageToDict(request)
        url_encoded_request = urlencode(json_request)
        response = self.rest_client.get(f"{self.txs_url_path}&{url_encoded_request}")
        return Parse(response, GetTxsEventResponse())
