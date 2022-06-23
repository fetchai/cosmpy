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
import time

from google.protobuf import any_pb2

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgExec
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


def main():

    wallet = LocalWallet(PrivateKey("F7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))
    task_wallet = LocalWallet(
        PrivateKey("HI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")
    )

    # authz_wallet must have authorization to send tokens from wallet. see aerial_authz.py
    authz_wallet = LocalWallet(
        PrivateKey("KI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")
    )

    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    # Set top-up amount
    amount = 10000000000000000
    top_up_amount = Coin(amount=str(amount), denom="atestfet")

    # Set minimum balance for task_wallet
    minimum_balance = 1000000000000000

    # Set interval to query task_wallet's balance
    interval_time = 5

    while True:

        wallet_balance = ledger.query_bank_balance(str(wallet.address()))

        if wallet_balance < amount:
            print("Wallet doesnt have enought balance to top-up task_wallet")
            break

        task_wallet_balance = ledger.query_bank_balance(str(task_wallet.address()))

        if task_wallet_balance < minimum_balance:

            print("topping up task wallet")
            # Top-up task_wallet
            msg = any_pb2.Any()
            msg.Pack(
                MsgSend(
                    from_address=str(wallet.address()),
                    to_address=str(task_wallet.address()),
                    amount=[top_up_amount],
                ),
                "",
            )

            tx = Transaction()
            tx.add_message(MsgExec(grantee=str(authz_wallet.address()), msgs=[msg]))

            tx = prepare_and_broadcast_basic_transaction(ledger, tx, authz_wallet)
            tx.wait_to_complete()

        time.sleep(interval_time)


if __name__ == "__main__":
    main()
