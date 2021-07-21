from cosm.common.rest_client import RestClient as RestClient
from cosm.tx.interface import RPCInterface

from cosmos.tx.v1beta1.service_pb2 import (
    SimulateRequest,
    SimulateResponse,
    GetTxRequest,
    GetTxResponse,
    BroadcastTxRequest,
    BroadcastTxResponse,
    GetTxsEventRequest,
    GetTxsEventResponse,
)
from google.protobuf.json_format import Parse


class TxRestClient(RPCInterface):
    txs_url_path = "/cosmos/tx/v1beta1/txs"

    def __init__(self, rest_client: RestClient):
        self.rest_client = rest_client

    # Simulate simulates executing a transaction for estimating gas usage.
    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        response = self.rest_client.post("/cosmos/tx/v1beta1/simulate", request)
        return Parse(response, SimulateResponse())

    # GetTx fetches a tx by hash.
    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        response = self.rest_client.get(self.txs_url_path, request)
        return Parse(response, GetTxResponse())

    # BroadcastTx broadcast transaction.
    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        response = self.rest_client.post(self.txs_url_path, request)
        return Parse(response, BroadcastTxResponse())

    # GetTxsEvent fetches txs by event.
    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        response = self.rest_client.get(self.txs_url_path, request)
        return Parse(response, GetTxsEventResponse())
