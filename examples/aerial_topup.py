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
import argparse
import time

from google.protobuf import any_pb2

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgExec
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("wallet_address", help="main wallet address")
    parser.add_argument(
        "task_wallet_address", help="wallet address that will perform transactions"
    )
    parser.add_argument(
        "top_up_amount",
        type=int,
        nargs="?",
        default=10000000000000000,
        help="top-up amount from wallet address to task_wallet address",
    )
    parser.add_argument(
        "minimum_balance",
        type=int,
        nargs="?",
        default=1000000000000000,
        help="minimum task_wallet address balance that will trigger top-up",
    )
    parser.add_argument(
        "interval_time",
        type=int,
        nargs="?",
        default=5,
        help="interval time in seconds to query task_wallet's balance",
    )

    return parser.parse_args()


def main():
    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    args = _parse_commandline()

    wallet_address = args.wallet_address

    task_wallet_address = args.task_wallet_address

    # Use aerial_authz.py to authorize authz_wallet address to send tokens from wallet
    authz_wallet = LocalWallet.generate()
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    wallet_balance = ledger.query_bank_balance(authz_wallet.address())

    while wallet_balance < (10**18):
        print("Providing wealth to wallet...")
        faucet_api.get_wealth(authz_wallet.address())
        wallet_balance = ledger.query_bank_balance(authz_wallet.address())

    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    # Top-up amount
    amount = args.top_up_amount
    top_up_amount = Coin(amount=str(amount), denom="atestfet")

    # Minimum balance for task_wallet
    minimum_balance = args.minimum_balance

    # Interval to query task_wallet's balance
    interval_time = args.interval_time

    while True:

        wallet_balance = ledger.query_bank_balance(wallet_address)

        if wallet_balance < amount:
            print("Wallet doesn't have enough balance to top-up task_wallet")
            break

        task_wallet_balance = ledger.query_bank_balance(task_wallet_address)

        if task_wallet_balance < minimum_balance:

            print("topping up task wallet")
            # Top-up task_wallet
            msg = any_pb2.Any()
            msg.Pack(
                MsgSend(
                    from_address=wallet_address,
                    to_address=task_wallet_address,
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
