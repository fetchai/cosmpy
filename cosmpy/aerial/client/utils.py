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
"""Helper functions."""
from datetime import timedelta
from typing import Any, Callable, List, Optional, Tuple, Union

from cosmpy.aerial.coins import parse_coins
from cosmpy.aerial.tx import SigningCfg, Transaction
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
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


def simulate_tx(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: Transaction,
    sender: "Wallet",  # type: ignore # noqa: F821
    account: "Account",  # type: ignore # noqa: F821
    memo: Optional[str] = None,
) -> Tuple[int, str]:
    """Estimate transaction fees based on either a provided amount, gas limit, or simulation.

    :param client: Ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param memo: Transaction memo, defaults to None

    :return: Estimated gas_limit and fee amount tuple
    """
    # we need to build up a representative transaction so that we can accurately simulate it
    tx.seal(
        SigningCfg.direct(sender.public_key(), account.sequence),
        fee=TxFee([], 0),
        memo=memo,
    )
    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    # simulate the gas and fee for the transaction
    gas_limit, fee = client.estimate_gas_and_fee_for_tx(tx)

    return gas_limit, fee


def prepare_and_broadcast_basic_transaction(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: "Transaction",  # type: ignore # noqa: F821
    sender: "Wallet",  # type: ignore # noqa: F821
    account: Optional["Account"] = None,  # type: ignore # noqa: F821
    fee: Optional[TxFee] = None,
    memo: Optional[str] = None,
    timeout_height: Optional[int] = None,
) -> SubmittedTx:
    """Prepare and broadcast basic transaction.

    :param client: Ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param fee: The tx fee
    :param memo: Transaction memo, defaults to None
    :param timeout_height: timeout height, defaults to None

    :return: broadcast transaction
    """
    if fee is None:
        fee, account = TxFee.from_simulation(
            client, tx, sender, account=account, memo=memo
        )

    # query the account information for the sender
    if account is None:
        account = client.query_account(sender.address())

    # Build the final transaction
    tx.seal(
        SigningCfg.direct(sender.public_key(), account.sequence),
        fee=fee,
        memo=memo,
        timeout_height=timeout_height,
    )
    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    return client.broadcast_tx(tx)


def ensure_timedelta(interval: Union[int, float, timedelta]) -> timedelta:
    """
    Return timedelta for interval.

    :param interval: timedelta or seconds in int or float

    :return: timedelta
    """
    return interval if isinstance(interval, timedelta) else timedelta(seconds=interval)


DEFAULT_PER_PAGE_LIMIT = None


def get_paginated(
    initial_request: Any,
    request_method: Callable,
    pages_limit: int = 0,
    per_page_limit: Optional[int] = DEFAULT_PER_PAGE_LIMIT,
) -> List[Any]:
    """
    Get pages for specific request.

    :param initial_request: request supports pagination
    :param request_method: function to perform request
    :param pages_limit: max number of pages to return. default - 0 unlimited
    :param per_page_limit: Optional int: amount of records per one page. default is None, determined by server

    :return: List of responses
    """
    pages: List[Any] = []
    pagination = PageRequest(limit=per_page_limit)

    while pagination and (len(pages) < pages_limit or pages_limit == 0):
        request = initial_request.__class__()
        request.CopyFrom(initial_request)
        request.pagination.CopyFrom(pagination)

        resp = request_method(request)

        pages.append(resp)

        pagination = None

        if resp.pagination.next_key:
            pagination = PageRequest(limit=per_page_limit, key=resp.pagination.next_key)
    return pages
