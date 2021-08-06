import json

from cosm.crypto.address import Address
from cosm.crypto.keypairs import PrivateKey
from cosm.common.rest_client import RestClient
from cosm.wasm.rest_client import WasmRestClient
from cosmwasm.wasm.v1beta1.query_pb2 import (
    QueryAllContractStateRequest,
    QueryAllContractStateResponse,
    QueryCodeRequest,
    QueryCodeResponse,
    QueryCodesRequest,
    QueryCodesResponse,
    QueryContractHistoryRequest,
    QueryContractHistoryResponse,
    QueryContractInfoRequest,
    QueryContractInfoResponse,
    QueryContractsByCodeRequest,
    QueryContractsByCodeResponse,
    QueryRawContractStateRequest,
    QueryRawContractStateResponse,
    QuerySmartContractStateRequest,
    QuerySmartContractStateResponse,
)

# Private key of sender's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)
VALIDATOR_ADDRESS = Address(VALIDATOR_PK)

TOKEN_ID = "1234"



REST_ENDPOINT_ADDRESS = "http://localhost:1317"

contract_address = "fetch1pcknsatx5ceyfu6zvtmz3yr8auumzrdt9vwz42"


channel = RestClient(REST_ENDPOINT_ADDRESS)
wasm_query_client = WasmRestClient(channel)


# Query validator's balance of token TOKEN_ID
msg = {"balance": {
    "address": str(VALIDATOR_ADDRESS),
    "id": TOKEN_ID,
}}


request = QuerySmartContractStateRequest(address=contract_address,
                                         query_data=json.dumps(msg).encode("UTF8"))
res = wasm_query_client.SmartContractState(request)

print(res)
