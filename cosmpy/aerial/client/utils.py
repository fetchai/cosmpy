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
        fee="",
        gas_limit=0,
        memo=memo,
    )
    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    # simulate the gas and fee for the transaction
    gas_limit, fee = client.estimate_gas_and_fee_for_tx(tx)

    return gas_limit, fee


def estimate_tx_fees(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: Transaction,
    sender: "Wallet",  # type: ignore # noqa: F821
    amount: Optional[str] = None,
    gas_limit: Optional[int] = None,
    granter: Optional[Address] = None,
    account: Optional["Account"] = None,  # type: ignore # noqa: F821
    memo: Optional[str] = None,
) -> Tuple[Fee, Optional["Account"]]:  # type: ignore # noqa: F821
    """Estimate transaction fees based on either a provided amount, gas limit, or simulation.

    :param client: Ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param amount: Transaction fee amount, defaults to None
    :param gas_limit: The gas limit
    :param granter: Transaction fee granter, defaults to None
    :param account: The account
    :param memo: Transaction memo, defaults to None

    :return: Fee object and queried account tuple
    """
    if gas_limit is None:
        # Ensure we have the account info
        account = account or client.query_account(sender.address())

        # Simulate transaction to get gas and amount
        gas_limit, estimated_amount = simulate_tx(client, tx, sender, account, memo)

        # Use estimated amount if not provided
        amount = amount or estimated_amount

    else:
        # Estimate amount based on provided gas if not already set
        amount = amount or client.estimate_fee_from_gas(gas_limit)

    fee = Fee(
        amount=parse_coins(amount),
        gas_limit=gas_limit,
        granter=granter,
    )

    return fee, account


def prepare_and_broadcast_basic_transaction(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: "Transaction",  # type: ignore # noqa: F821
    sender: "Wallet",  # type: ignore # noqa: F821
    account: Optional["Account"] = None,  # type: ignore # noqa: F821
    gas_limit: Optional[int] = None,
    memo: Optional[str] = None,
    timeout_height: Optional[int] = None,
    fee_amount: Optional[str] = None,
    fee_granter: Optional[Address] = None,
) -> SubmittedTx:
    """Prepare and broadcast basic transaction.

    :param client: Ledger client
    :param tx: The transaction
    :param sender: The transaction sender
    :param account: The account
    :param gas_limit: The gas limit
    :param memo: Transaction memo, defaults to None
    :param timeout_height: timeout height, defaults to None
    :param fee_amount: Transaction fee amount, defaults to None
    :param fee_granter: Transaction fee granter, defaults to None

    :return: broadcast transaction
    """
    fee, account = estimate_tx_fees(
        client, tx, sender, fee_amount, gas_limit, fee_granter, account, memo
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
