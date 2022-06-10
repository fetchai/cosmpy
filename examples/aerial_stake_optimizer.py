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

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.client.distribution import create_withdraw_delegator_reward
from cosmpy.aerial.client.staking import create_delegate_msg
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx import SigningCfg, Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryTotalSupplyRequest
from cosmpy.protos.cosmos.params.v1beta1.query_pb2 import QueryParamsRequest
from cosmpy.protos.cosmos.staking.v1beta1.query_pb2 import QueryValidatorsRequest


def M(x, f, S, k, D):
    return (S * (1 + (k * x)) ** (D / x)) + (
        (1 - ((1 + (k * x)) ** (D / x))) / (k * x)
    ) * f


def main():
    ledger = LedgerClient(NetworkConfig.fetchai_dorado_testnet())

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

    # Choose a validator
    validators = ledger.query_validators()
    validator = validators[0]

    # Query validator commission
    commission = float(resp.validators[0].commission.commission_rates.rate) / 1e18

    # Set percentage delegated of total stake
    pctDelegatedOfTotalStake = initial_stake / total_stake

    # Estmate fees for claiming and delegating rewards

    # Use any address with tokens available
    key = PrivateKey("XZ5BZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV7=")
    alice = LocalWallet(key)
    alice_address = Address(key)._display

    tx = Transaction()

    # Add delegate msg
    tx.add_message(
        create_delegate_msg(alice_address, validator.address, initial_stake, "atestfet")
    )

    # Add claim reward msg
    tx.add_message(create_withdraw_delegator_reward(alice_address, validator.address))

    account = ledger.query_account(alice.address())

    tx.seal(
        SigningCfg.direct(alice.public_key(), account.sequence), fee="", gas_limit=0
    )
    tx.sign(alice.signer(), ledger.network_config.chain_id, account.number)
    tx.complete()

    # simulate the fee for the transaction
    _, str_tx_fee = ledger.estimate_gas_and_fee_for_tx(tx)

    denom = "atestfet"
    tx_fee = str_tx_fee[: -len(denom)]

    # Round up to get a conservative estimate
    fee = round(int(tx_fee), -len(tx_fee) + 1)

    # Query chain variables

    # Total Supply of tokens
    req = QueryTotalSupplyRequest()
    resp = ledger.bank.TotalSupply(req)
    totalSupply = float(json.loads(resp.supply[0].amount))

    # Inflation
    req = QueryParamsRequest(subspace="mint", key="InflationRate")
    resp = ledger.params.Params(req)
    inflation = float(json.loads(resp.param.value))

    # Community Tax
    req = QueryParamsRequest(subspace="distribution", key="communitytax")
    resp = ledger.params.Params(req)
    communityTax = float(json.loads(resp.param.value))

    # Anual reward calculation
    anualDelegatorReward = (
        (inflation * totalSupply)
        * pctDelegatedOfTotalStake
        * (1 - communityTax)
        * (1 - commission)
    )

    # Convert from anual reward to minute reward
    minuteReward = anualDelegatorReward / 360 / 24 / 60
    rate = minuteReward / initial_stake

    # Compute optimal period
    f = fee
    S = initial_stake
    k = rate
    D = total_period

    # List of compounding periods
    X = [i for i in range(1, D)]

    # Evaluate function M on each compounding period
    R = [M(x, f, S, k, D) for x in X]

    # Fnd the period that maximizes rewards
    optimal_period = R.index(max(R)) + 1

    # These values can be used in aerial_compounder.py to maximize rewards
    print("total period: ", total_period, "minutes")
    print("optimal compounding period: ", optimal_period, "minutes")


if __name__ == "__main__":
    main()
