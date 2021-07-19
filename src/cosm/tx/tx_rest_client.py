from cosm.query.rest_client import RestClient
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
from google.protobuf.json_format import MessageToDict, Parse
import urllib


class TxRestClient(RPCInterface):
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    # Simulate simulates executing a transaction for estimating gas usage.
    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        json_request = MessageToDict(request)
        response = self.rest_api.post(
            f"/cosmos/tx/v1beta1/simulate",
            json_request
            )
        return Parse(response, SimulateResponse())

    # GetTx fetches a tx by hash.
    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        json_request = MessageToDict(request)
        url_encoded_request = urllib.urlencode(json_request)
        response = self.rest_api.get(
            f"/cosmos/tx/v1beta1/txs&{url_encoded_request}",
            )
        return Parse(response, GetTxResponse())

    # BroadcastTx broadcast transaction.
    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        json_request = MessageToDict(request)
        response = self.rest_api.post(
            f"/cosmos/tx/v1beta1/txs",
            json_request
        )
        return Parse(response, BroadcastTxResponse())

    # GetTxsEvent fetches txs by event.
    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        json_request = MessageToDict(request)
        url_encoded_request = urllib.urlencode(json_request)
        response = self.rest_api.get(
            f"/cosmos/tx/v1beta1/txs&{url_encoded_request}"
            )
        return Parse(response, GetTxsEventResponse())
