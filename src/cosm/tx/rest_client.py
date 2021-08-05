import json
import base64

from common import JSONLike
from typing import List
from cosm.query.rest_client import QueryRestClient as RestClient
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
from google.protobuf.json_format import MessageToDict, Parse, ParseDict
from urllib.parse import urlencode


class TxRestClient(RPCInterface):
    txs_url_path = "/cosmos/tx/v1beta1/txs"

    def __init__(self, rest_client: RestClient):
        """
        Tx REST client

        :param rest_client: REST api client
        """
        self.rest_client = rest_client

    def Simulate(self, request: SimulateRequest) -> SimulateResponse:
        """
        Simulate simulates executing a transaction for estimating gas usage.

        :param request: SimulateRequest
        :return: SimulateResponse
        """
        json_request = MessageToDict(request)
        response = self.rest_client.post("/cosmos/tx/v1beta1/simulate", json_request)
        return Parse(response, SimulateResponse())

    def GetTx(self, request: GetTxRequest) -> GetTxResponse:
        """
        GetTx fetches a tx by hash.

        :param request: GetTxRequest
        :return: GetTxResponse
        """
        json_request = MessageToDict(request)
        json_request.pop("hash")
        url_encoded_request = urlencode(json_request)
        response = self.rest_client.get(
            f"{self.txs_url_path}/{request.hash}?{url_encoded_request}",
        )

        # JSON in JSON in case of CosmWasm messages workaround
        dict_response = json.loads(response)
        self._fix_messages(dict_response["tx"]["body"]["messages"])
        self._fix_messages(dict_response["tx_response"]["tx"]["body"]["messages"])

        return ParseDict(dict_response, GetTxResponse())

    def BroadcastTx(self, request: BroadcastTxRequest) -> BroadcastTxResponse:
        """
        BroadcastTx broadcast transaction.

        :param request: BroadcastTxRequest
        :return: BroadcastTxResponse
        """
        json_request = MessageToDict(request)
        response = self.rest_client.post(self.txs_url_path, json_request)
        return Parse(response, BroadcastTxResponse())

    def GetTxsEvent(self, request: GetTxsEventRequest) -> GetTxsEventResponse:
        """
        GetTxsEvent fetches txs by event.

        :param request: GetTxsEventRequest
        :return: GetTxsEventResponse
        """
        json_request = MessageToDict(request)
        url_encoded_request = urlencode(json_request)
        response = self.rest_client.get(f"{self.txs_url_path}&{url_encoded_request}")
        return Parse(response, GetTxsEventResponse())

    @staticmethod
    def _fix_messages(messages: List[JSONLike]):
        """
        Fix for REST api response in case of CosmWasm messages contains dict instead of base64 encoded string

        :param messages: List of message in Tx response
        """
        for message in messages:
            if message["@type"] == "/cosmwasm.wasm.v1beta1.MsgInstantiateContract":
                message["init_msg"] = base64.b64encode(
                    json.dumps(message["init_msg"]).encode("UTF8")
                ).decode()
            if message["@type"] == "/cosmwasm.wasm.v1beta1.MsgExecuteContract":
                message["msg"] = base64.b64encode(
                    json.dumps(message["msg"]).encode("UTF8")
                ).decode()
