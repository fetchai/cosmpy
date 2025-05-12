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

"""Transaction helpers."""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from cosmpy.aerial.client.utils import simulate_tx
from cosmpy.aerial.coins import parse_coins
from cosmpy.aerial.exceptions import (
    BroadcastError,
    InsufficientFeesError,
    OutOfGasError,
)
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import Fee


class TxFee:
    """Cosmos SDK TxFee abstraction."""

    def __init__(
        self,
        amount: List["Coin"],  # type: ignore # noqa: F821
        gas_limit: int,
        granter: Optional[Address] = None,
        payer: Optional[Address] = None,
    ):
        """Init the Transaction fee class.

        :param amount: tx fee amount
        :param gas_limit: gas limit
        :param granter: transaction fee granter, defaults to None
        :param payer: transaction fee payer, defaults to None
        :returns initialised TxFee
        """
        self.amount = amount
        self.gas_limit = gas_limit
        self.granter = granter
        self.payer = payer

    @classmethod
    def from_fixed_amount(
        cls,
        amount: str,
        gas_limit: int = 0,
        granter: Optional[Address] = None,
        payer: Optional[Address] = None,
    ) -> "TxFee":
        """Init the Transaction fee class from string amount.

        :param amount: tx fee amount string
        :param gas_limit: gas limit
        :param granter: transaction fee granter, defaults to None
        :param payer: transaction fee payer, defaults to None
        :return: TxFee
        """
        return cls(
            amount=parse_coins(amount),
            gas_limit=gas_limit,
            granter=granter,
            payer=payer,
        )

    @classmethod
    def from_gas_only(
        cls,
        client: "LedgerClient",  # type: ignore # noqa: F821
        gas_limit: int,
        granter: Optional[Address] = None,
        payer: Optional[Address] = None,
    ) -> "TxFee":
        """Init the Transaction fee class from gas limit.

        :param client: Ledger client
        :param gas_limit: gas limit
        :param granter: transaction fee granter, defaults to None
        :param payer: transaction fee payer, defaults to None
        :return: TxFee
        """
        estimated_amount = client.estimate_fee_from_gas(gas_limit)
        return cls(
            amount=parse_coins(estimated_amount),
            gas_limit=gas_limit,
            granter=granter,
            payer=payer,
        )

    @classmethod
    def from_simulation(
        cls,
        client: "LedgerClient",  # type: ignore # noqa: F821
        tx: "Transaction",  # type: ignore  # noqa: F821
        sender: "Wallet",  # type: ignore # noqa: F821
        amount: Optional[str] = None,
        granter: Optional[Address] = None,
        payer: Optional[Address] = None,
        account: Optional["Account"] = None,  # type: ignore # noqa: F821
        memo: Optional[str] = None,
    ) -> Tuple[Fee, Optional["Account"]]:  # type: ignore # noqa: F821
        """Estimate transaction fees based on either a provided amount, gas limit, or simulation.

        :param client: Ledger client
        :param tx: The transaction
        :param sender: The transaction sender
        :param amount: Transaction fee amount, defaults to None
        :param granter: Transaction fee granter, defaults to None
        :param payer: Transaction fee payer, defaults to None
        :param account: The account
        :param memo: Transaction memo, defaults to None
        :return: TxFee
        """
        # Ensure we have the account info
        account = account or client.query_account(sender.address())

        # Simulate transaction to get gas and amount
        gas_limit, estimated_amount = simulate_tx(client, tx, sender, account, memo)

        # Use estimated amount if not provided
        amount = amount or estimated_amount

        fee = Fee(
            amount=parse_coins(amount),
            gas_limit=gas_limit,
            granter=granter,
            payer=payer,
        )

        return fee, account

    def to_pb_fee(self) -> Fee:
        """Return protobuf representation of TxFee.

        :return: Fee
        """
        return Fee(
            amount=self.amount,
            gas_limit=self.gas_limit,
            granter=self.granter,
            payer=self.payer,
        )


@dataclass
class MessageLog:
    """Message Log."""

    index: int  # noqa
    log: str  # noqa
    events: Dict[str, Dict[str, str]]


@dataclass
class TxResponse:
    """Transaction response.

    :raises OutOfGasError: Out of gas error
    :raises InsufficientFeesError: Insufficient fees
    :raises BroadcastError: Broadcast Exception
    """

    hash: str
    height: int
    code: int
    gas_wanted: int
    gas_used: int
    raw_log: str
    logs: List[MessageLog]
    events: Dict[str, Dict[str, str]]
    timestamp: Optional[datetime]

    def is_successful(self) -> bool:
        """Check transaction is successful.

        :return: transaction status
        """
        return self.code == 0

    def ensure_successful(self):
        """Ensure transaction is successful.

        :raises OutOfGasError: Out of gas error
        :raises InsufficientFeesError: Insufficient fees
        :raises BroadcastError: Broadcast Exception
        """
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
            if "insufficient fees" in self.raw_log:
                match = re.search(r"required:\s*(\d+\w+)", self.raw_log)
                if match is not None:
                    required_fee = match.group(1)
                else:
                    required_fee = f"more than {self.gas_wanted}"
                raise InsufficientFeesError(self.hash, required_fee)
            raise BroadcastError(self.hash, self.raw_log)


class SubmittedTx:
    """Submitted transaction."""

    def __init__(
        self, client: "LedgerClient", tx_hash: str  # type: ignore # noqa: F821
    ):
        """Init the Submitted transaction.

        :param client: Ledger client
        :param tx_hash: transaction hash
        """
        self._client = client
        self._response: Optional[TxResponse] = None
        self._tx_hash = str(tx_hash)

    @property
    def tx_hash(self) -> str:
        """Get the transaction hash.

        :return: transaction hash
        """
        return self._tx_hash

    @property
    def response(self) -> Optional[TxResponse]:
        """Get the transaction response.

        :return: response
        """
        return self._response

    @property
    def contract_code_id(self) -> Optional[int]:
        """Get the contract code id.

        :return: return contract code id if exist else None
        """
        if self._response is None:
            return None

        code_id = self._response.events.get("store_code", {}).get("code_id")
        if code_id is None:
            return None

        return int(code_id)

    @property
    def contract_address(self) -> Optional[Address]:
        """Get the contract address.

        :return: return contract address if exist else None
        """
        if self._response is None:
            return None

        contract_address = self._response.events.get("instantiate", {}).get(
            "_contract_address"
        )
        if contract_address is None:
            return None

        return Address(contract_address)

    def wait_to_complete(
        self,
        timeout: Optional[Union[int, float, timedelta]] = None,
        poll_period: Optional[Union[int, float, timedelta]] = None,
    ) -> "SubmittedTx":
        """Wait to complete the transaction.

        :param timeout: timeout, defaults to None
        :param poll_period: poll_period, defaults to None

        :return: Submitted Transaction
        """
        self._response = self._client.wait_for_query_tx(
            self.tx_hash, timeout=timeout, poll_period=poll_period
        )
        assert self._response is not None
        self._response.ensure_successful()

        return self
