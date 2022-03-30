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
import random

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


def _wait_for_tx(operation: str, tx: SubmittedTx):
    print(f"Waiting for {operation} to complete... (tx: {tx.tx_hash})")
    tx.wait_to_complete()
    print(f"Waiting for {operation} to complete... done")


def main():
    alice = LocalWallet(PrivateKey("T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))

    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    # get all the active validators on the network
    validators = ledger.query_validators()

    # randomly choose one to stake to (this is a BAD idea generally, but fine for this example)
    first_validator = random.choice(validators)  # nosec

    # delegate some tokens to this validator
    tx = ledger.delegate_tokens(first_validator.address, 20, alice)
    _wait_for_tx("delegate", tx)

    # select another validator to redelegate to (again, not a good idea in general)
    second_validator = random.choice(  # nosec
        list(
            filter(
                lambda v: v.address != first_validator.address,
                validators,
            )
        )
    )

    # redelegate the tokens
    tx = ledger.redelegate_tokens(
        first_validator.address, second_validator.address, 10, alice
    )
    _wait_for_tx("redelegate", tx)

    # undelegate the tokens
    tx = ledger.undelegate_tokens(first_validator.address, 5, alice)
    _wait_for_tx("undelegate", tx)

    summary = ledger.query_staking_summary(alice.address())
    print(
        f"Summary: Staked: {summary.total_staked} Unbonding: {summary.total_unbonding} Rewards: {summary.total_rewards}"
    )

    # finally, lets collect up all the rewards we have earned so far
    claimed = False
    for position in summary.current_positions:
        if position.reward > 0:
            claimed = True

            tx = ledger.claim_rewards(position.validator, alice)
            _wait_for_tx(f"claim from {str(position.validator)}", tx)

    if claimed:
        summary = ledger.query_staking_summary(alice.address())
        print(
            f"Summary: Staked: {summary.total_staked} Unbonding: {summary.total_unbonding} Rewards: {summary.total_rewards}"
        )


if __name__ == "__main__":
    main()
