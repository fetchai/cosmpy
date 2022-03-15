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

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from cosmpy.aerial.exceptions import (
    BroadcastError,
    InsufficientFeesError,
    OutOfGasError,
)
from cosmpy.crypto.address import Address


@dataclass
class MessageLog:
    index: int  # noqa
    log: str  # noqa
    events: Dict[str, Dict[str, str]]


@dataclass
class TxResponse:
    hash: str
    height: int
    code: int
    gas_wanted: int
    gas_used: int
    raw_log: str
    logs: List[MessageLog]
    events: Dict[str, Dict[str, str]]

    def is_successful(self) -> bool:
        return self.code == 0

    def ensure_successful(self):
        if self.code != 0:
            if "out of gas" in self.raw_log:
                match = re.search(
                    r"gasWanted:\s*(\d+).*?gasUsed:\s*(\d+)", self.raw_log
                )
                if match is not None:
                    gas_wanted = int(match.group(1))
                    gas_used = int(match.group(2))
                else:
                    gas_wanted = -1
                    gas_used = -1

                raise OutOfGasError(self.hash, gas_wanted=gas_wanted, gas_used=gas_used)
            elif "insufficient fees" in self.raw_log:
                match = re.search(r"required:\s*(\d+\w+)", self.raw_log)
                if match is not None:
                    required_fee = match.group(1)
                else:
                    required_fee = f"more than {self.gas_wanted}"
                raise InsufficientFeesError(self.hash, required_fee)
            else:
                raise BroadcastError(self.hash, self.raw_log)


class SubmittedTx:
    def __init__(
        self, client: "LedgerClient", tx_hash: str  # type: ignore # noqa: F821
    ):
        self._client = client
        self._response: Optional[TxResponse] = None
        self._tx_hash = str(tx_hash)

    @property
    def tx_hash(self) -> str:
        return self._tx_hash

    @property
    def response(self) -> Optional[TxResponse]:
        return self._response

    @property
    def contract_code_id(self) -> Optional[int]:
        if self._response is None:
            return None

        code_id = self._response.events.get("store_code", {}).get("code_id")
        if code_id is None:
            return None

        return int(code_id)

    @property
    def contract_address(self) -> Optional[Address]:
        if self._response is None:
            return None

        contract_address = self._response.events.get("instantiate", {}).get(
            "_contract_address"
        )
        if contract_address is None:
            return None

        return Address(contract_address)

    def wait_to_complete(self) -> "SubmittedTx":
        self._response = self._client.wait_for_query_tx(self.tx_hash)
        assert self._response is not None
        self._response.ensure_successful()

        return self
