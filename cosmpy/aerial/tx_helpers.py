from dataclasses import dataclass
from typing import Dict, List, Optional

from cosmpy.crypto.address import Address


@dataclass
class MessageLog:
    index: int
    log: str
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


class SubmittedTx:
    def __init__(self, client: "LedgerClient", tx_hash: str):
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
        if not self._response.is_successful():
            raise RuntimeError(
                f"Transaction was unsuccessful (code: {self._response.code} tx: {self._response.hash})"
            )
        return self
