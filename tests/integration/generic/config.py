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

"""Module with config used in Fetchd integration tests."""

import inspect
import os
from pathlib import Path

from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# Denomination and amount of transferred tokens
DENOM = "stake"
AMOUNT = 1
COINS = [Coin(amount=str(AMOUNT), denom=DENOM)]

# Node config
GRPC_ENDPOINT_ADDRESS = "localhost:9090"
REST_ENDPOINT_ADDRESS = "http://localhost:1317"
CHAIN_ID = "testing"

# Private key of sender account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex("0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae")
)
VALIDATOR_ADDRESS = Address(VALIDATOR_PK)

# Private key of recipient account
BOB_PK = PrivateKey(
    bytes.fromhex("439861b21d146e83fe99496f4998a305c83cfbc24717c77e32b06d224bf1e636")
)
BOB_ADDRESS = Address(BOB_PK)

# Cosmwasm
CUR_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
CONTRACT_FILENAME = Path(
    os.path.join(CUR_PATH, "..", "..", "..", "contracts", "cw_erc1155.wasm")
)
TOKEN_ID = "680564733841876926926749214863536422914"  # nosec
