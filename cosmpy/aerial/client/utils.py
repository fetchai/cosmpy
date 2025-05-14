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
from typing import Any, Callable, List, Optional, Union

from cosmpy.aerial.tx import Transaction, TxFee
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest


def prepare_and_broadcast_basic_transaction(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: Transaction,
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
        fee = TxFee()

    # query the account information for the sender
    if account is None:
        account = client.query_account(sender.address())

    # Build the final transaction
    tx.online_seal(
        client,
        sender,
        fee=fee,
        account=account,
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
