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
from datetime import datetime, timedelta

from google.protobuf import any_pb2, timestamp_pb2

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import GenericAuthorization, Grant
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgExec, MsgGrant
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


def main():

    # Set main wallet
    wallet = LocalWallet(PrivateKey("F7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))

    # Set task wallet [will perform transactions]
    task_wallet = LocalWallet(
        PrivateKey("HI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")
    )

    # Set authz wallet [will top-up task_wallet from wallet]
    authz_wallet = LocalWallet(
        PrivateKey("KI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")
    )

    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    # Set authorization time for authz_wallet in minutes
    total_authz_time = 1000

    # Authorize authz_wallet to send tokens from wallet
    authz_any = any_pb2.Any()
    authz_any.Pack(
        GenericAuthorization(msg="/cosmos.bank.v1beta1.MsgSend"),
        "",
    )

    expiry = timestamp_pb2.Timestamp()
    expiry.FromDatetime(datetime.now() + timedelta(seconds=total_authz_time * 60))
    grant = Grant(authorization=authz_any, expiration=expiry)

    msg = MsgGrant(
        granter=str(wallet.address()),
        grantee=str(authz_wallet.address()),
        grant=grant,
    )

    tx = Transaction()
    tx.add_message(msg)

    tx = prepare_and_broadcast_basic_transaction(ledger, tx, wallet)
    tx.wait_to_complete()

    # Set top-up amount
    amount = 10000000000000000
    top_up_amount = Coin(amount=str(amount), denom="atestfet")

    # Choose any validator
    validators = ledger.query_validators()
    validator = validators[0]

    # Set minimum balance for task_wallet
    minimum_balance = 1000000000000000

    while True:

        wallet_balance = ledger.query_bank_balance(str(wallet.address()))

        if wallet_balance < amount:
            print("Wallet doesnt have enough balance to top-up task_wallet")
            break

        task_wallet_balance = ledger.query_bank_balance(str(task_wallet.address()))

        if task_wallet_balance < minimum_balance:

            # Top-up task_wallet
            print("topping up task wallet")
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

        # Perform delegation transactions from task_wallet to deplete its balance
        print("task_wallet > performing transaction: delegating tokens")
        tx = ledger.delegate_tokens(validator.address, 100, task_wallet)
        tx.wait_to_complete()

        time.sleep(5)


if __name__ == "__main__":
    main()
