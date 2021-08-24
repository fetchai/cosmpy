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

"""Implementation of CosmWasm query client."""

import json
from typing import Union

from grpc._channel import Channel

from cosmpy.auth.rest_client import AuthRestClient
from cosmpy.bank.rest_client import BankRestClient
from cosmpy.common.rest_client import RestClient
from cosmpy.common.types import JSONLike
from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2_grpc import QueryStub as AuthGrpcClient
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import (
    QueryBalanceRequest,
    QueryBalanceResponse,
)
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankGrpcClient
from cosmpy.protos.cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest
from cosmpy.protos.cosmwasm.wasm.v1beta1.query_pb2_grpc import (
    QueryStub as CosmWasmGrpcClient,
)


class CosmWasmClient:
    """High level client for REST/gRPC node interaction."""

    def __init__(self, channel: Union[Channel, RestClient]):
        """
        :param channel: gRPC or REST querying client

        :raises RuntimeError: if channel is of wrong type.
        """

        if isinstance(channel, Channel):
            self.bank_client: Union[BankRestClient, BankGrpcClient] = BankGrpcClient(
                channel
            )
            self.auth_client: Union[AuthRestClient, AuthGrpcClient] = AuthGrpcClient(
                channel
            )
            self.wasm_client: Union[
                CosmWasmRestClient, CosmWasmGrpcClient
            ] = CosmWasmGrpcClient(channel)
        elif isinstance(channel, RestClient):
            self.bank_client = BankRestClient(channel)
            self.auth_client = AuthRestClient(channel)
            self.wasm_client = CosmWasmRestClient(channel)
        else:
            raise RuntimeError(f"Unsupported channel type {type(channel)}")

    def get_balance(self, address: Address, denom: str) -> QueryBalanceResponse:
        """
        Get balance of specific account and denom

        :param address: Address
        :param denom: Denomination

        :return: QueryBalanceResponse
        """
        res = self.bank_client.Balance(
            QueryBalanceRequest(address=str(address), denom=denom)
        )
        return res

    def query_account_data(self, address: Address) -> BaseAccount:
        """
        Query account data for signing

        :param address: Address of account to query data about

        :raises TypeError: in case of wrong account type.

        :return: BaseAccount
        """
        # Get account data for signing
        account_response = self.auth_client.Account(
            QueryAccountRequest(address=str(address))
        )
        account = BaseAccount()
        if account_response.account.Is(BaseAccount.DESCRIPTOR):
            account_response.account.Unpack(account)
        else:
            raise TypeError("Unexpected account type")
        return account

    def query_contract_state(self, contract_address: str, msg: JSONLike) -> JSONLike:
        """
        Get state of smart contract

        :param contract_address: Contract address
        :param msg: Parameters to be passed to query function inside contract

        :return: JSON query response
        """
        request = QuerySmartContractStateRequest(
            address=contract_address, query_data=json.dumps(msg).encode("UTF8")
        )
        res = self.wasm_client.SmartContractState(request)
        return json.loads(res.data)
