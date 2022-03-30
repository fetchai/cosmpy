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
from typing import Optional

from cosmpy.aerial.tx import SigningCfg
from cosmpy.aerial.tx_helpers import SubmittedTx


def prepare_and_broadcast_basic_transaction(
    client: "LedgerClient",  # type: ignore # noqa: F821
    tx: "Transaction",  # type: ignore # noqa: F821
    sender: "Wallet",  # type: ignore # noqa: F821
    account: Optional["Account"] = None,  # type: ignore # noqa: F821
    gas_limit: Optional[int] = None,
    memo: Optional[str] = None,
) -> SubmittedTx:
    # query the account information for the sender
    if account is None:
        account = client.query_account(sender.address())

    if gas_limit is not None:
        # simply build the fee from the provided gas limit
        fee = client.estimate_fee_from_gas(gas_limit)
    else:

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

    # finally, build the final transaction that will be executed with the correct gas and fee values
    tx.seal(
        SigningCfg.direct(sender.public_key(), account.sequence),
        fee=fee,
        gas_limit=gas_limit,
        memo=memo,
    )
    tx.sign(sender.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    return client.broadcast_tx(tx)
