"""Example of aerial stake optimizer."""

# pylint: disable=too-many-locals

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
import json

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.client.distribution import create_withdraw_delegator_reward
from cosmpy.aerial.client.staking import create_delegate_msg
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.tx import SigningCfg, Transaction, TxFee
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryTotalSupplyRequest
from cosmpy.protos.cosmos.params.v1beta1.query_pb2 import QueryParamsRequest
from cosmpy.protos.cosmos.staking.v1beta1.query_pb2 import QueryValidatorsRequest


# This function returns the total reward for given:
# * f -> fee
# * s -> Initial Stake
# * k -> Reward Rate
# * d -> Total staking period
# * x -> Compounding Period
def calculate_total_rewards_for_period(x, f, s, k, d):
    """
    Calculate the total reward.

    :param x: Compounding Period
    :param f: fee
    :param s: Initial Stake
    :param k: Reward Rate
    :param d: Total staking period

    :return: Total reward
    """
    return (s * (1 + (k * x)) ** (d / x)) + (
        (1 - ((1 + (k * x)) ** (d / x))) / (k * x)
    ) * f


def main():
    """Run main."""
    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    # Set initial stake and desired stake period
    initial_stake = 50000000000000000000
    total_period = 60000

    req = QueryValidatorsRequest()
    resp = ledger.staking.Validators(req)

    # Calculate the total staked in the testnet

    total_stake = 0
    # validator.status == 3 refers to bonded validators
    validators_stake = [
        int(validator.tokens) for validator in resp.validators if validator.status == 3
    ]
    total_stake = sum(validators_stake)

    # Get validators commissions
    validators_commission = [
        float(validator.commission.commission_rates.rate)
        for validator in resp.validators
        if validator.status == 3
    ]

    validators = ledger.query_validators()
    validator = "not_selected"

    # Choose a threshold for a validators minimum percentage of total stake delegated
    stake_threshold = 0.10

    for _i in range(len(validators_commission)):
        # Choose validator with lower commission
        validator_index = validators_commission.index(min(validators_commission))

        # Verify that it meets the minimum % threshold
        validator_stake_pct = validators_stake[validator_index] / total_stake
        if validator_stake_pct >= stake_threshold:
            # Set the selected validator
            validator = validators[validator_index]
            break

        # We omit this validator by setting his commission to the maximum
        validators_commission[validator_index] = float("inf")

    if validator == "not_selected":
        # Restart validators_commission list with original values
        validators_commission = [
            float(validator.commission.commission_rates.rate)
            for validator in resp.validators
            if validator.status == 3
        ]

        print("No validator meets the minimum stake threshold requirement")

        # Proceed to select the validator with the lowest commission
        validator_index = validators_commission.index(min(validators_commission))
        validator = validators[validator_index]

    # Query validator commission
    commission = float(resp.validators[0].commission.commission_rates.rate) / 1e18

    # Set percentage delegated of total stake
    pct_delegated = initial_stake / total_stake

    # Estimate fees for claiming and delegating rewards

    alice = LocalWallet.generate()
    alice_address = alice.address()

    alice_balance = ledger.query_bank_balance(alice.address())

    while alice_balance < initial_stake:
        print("Providing wealth to alice...")
        faucet_api.get_wealth(alice.address())
        alice_balance = ledger.query_bank_balance(alice.address())

    tx = Transaction()

    # Add delegate msg
    tx.add_message(
        create_delegate_msg(alice_address, validator.address, initial_stake, "atestfet")
    )

    # Add claim reward msg
    tx.add_message(create_withdraw_delegator_reward(alice_address, validator.address))

    account = ledger.query_account(alice.address())

    tx.seal(SigningCfg.direct(alice.public_key(), account.sequence), TxFee([], 0))
    tx.sign(alice.signer(), ledger.network_config.chain_id, account.number)
    tx.complete()

    # simulate the fee for the transaction
    _, str_tx_fee = ledger.estimate_gas_and_fee_for_tx(tx)

    denom = "atestfet"
    tx_fee = str_tx_fee[: -len(denom)]

    # Add a 20% to the fee estimation to get a more conservative estimate
    fee = int(tx_fee) * 1.20

    # Query chain variables

    # Total Supply of tokens
    req = QueryTotalSupplyRequest()
    resp = ledger.bank.TotalSupply(req)
    total_supply = float(json.loads(resp.supply[0].amount))

    # Inflation
    req = QueryParamsRequest(subspace="mint", key="InflationRate")
    resp = ledger.params.Params(req)
    inflation = float(json.loads(resp.param.value))

    # Community Tax
    req = QueryParamsRequest(subspace="distribution", key="communitytax")
    resp = ledger.params.Params(req)
    community_tax = float(json.loads(resp.param.value))

    # Annual reward calculation
    annual_reward = (
        (inflation * total_supply)
        * pct_delegated
        * (1 - community_tax)
        * (1 - commission)
    )

    # Convert from annual reward to minute reward
    minute_reward = annual_reward / 360 / 24 / 60
    rate = minute_reward / initial_stake

    # Compute optimal period
    f = fee
    s = initial_stake
    k = rate
    d = total_period

    # List of compounding periods
    compounding_periods = list(range(1, d))

    # Evaluate function M on each compounding period
    total_rewards = [
        calculate_total_rewards_for_period(x, f, s, k, d) for x in compounding_periods
    ]

    # Fnd the period that maximizes rewards
    optimal_period = total_rewards.index(max(total_rewards)) + 1

    # These values can be used in aerial_compounder.py to maximize rewards
    print("total period: ", total_period, "minutes")
    print("optimal compounding period: ", optimal_period, "minutes")


if __name__ == "__main__":
    main()
