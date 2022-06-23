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
from datetime import datetime, timedelta

from google.protobuf import any_pb2, timestamp_pb2

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import GenericAuthorization, Grant
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgGrant


def main():

    wallet = LocalWallet(PrivateKey("F7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))

    # Set authz_wallet that will be granted authorization to send tokens from wallet
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


if __name__ == "__main__":
    main()
