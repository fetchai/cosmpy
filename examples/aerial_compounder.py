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

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


def main():
    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())

    # get all the active validators on the network
    validators = ledger.query_validators()

    # choose any validator
    validator = validators[0]

    key = PrivateKey("FX5BZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV7=")
    alice = LocalWallet(key)

    # delegate some tokens to this validator
    initial_stake = 9000000000000000000
    tx = ledger.delegate_tokens(validator.address, initial_stake, alice)
    tx.wait_to_complete()

    # set time limit and compounding period in seconds
    time_limit = 600
    period = 100

    time_check = 0
    start_time = time.monotonic()
    time.sleep(period)

    # query, claim and stake rewards after time period
    while time_check < time_limit:

        begin = time.monotonic()

        summary = ledger.query_staking_summary(alice.address())
        print(f"Staked: {summary.total_staked}")

        balance_before = ledger.query_bank_balance(alice.address())

        tx = ledger.claim_rewards(validator.address, alice)
        tx.wait_to_complete()

        balance_after = ledger.query_bank_balance(alice.address())

        # reward after any fees
        true_reward = balance_after - balance_before

        if true_reward > 0:

            print(f"Staking {true_reward} (reward after fees)")

            tx = ledger.delegate_tokens(validator.address, true_reward, alice)
            tx.wait_to_complete()

        else:
            print("Fees from claim rewards transaction exceeded reward")

        print()

        end = time.monotonic()
        time.sleep(period - (end - begin))
        time_check = time.monotonic() - start_time


if __name__ == "__main__":
    main()
