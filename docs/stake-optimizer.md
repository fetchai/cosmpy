When you delegate tokens to a validator for a determined period, you can use the [`auto-compounder`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_compounder.py) to get increasing rewards. You can maximize your rewards for a given staking period by selecting an optimal compounding period. To do this, you will need to follow these steps:

* **Set and Query Variables**: When calculating staking rewards, you need to set and query variables such as staking parameters, transaction fees, and network parameters
* **Calculate Reward Rate**: After you select and query all the variables needed, you will calculate the reward rate
* **Calculate Optimal Compounding Period**: You will calculate the optimal compounding period that will maximize your rewards

First, you need to define a network to work with.

```python
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig

ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
```

## Set and Query Variables

### Staking Variables

First, we need to define the desired amount and the total period that we would like to stake in:
`initial_stake` and `total_period` variables. Here we will stake 50 TESTFET for 60000 minutes. For this guide, we will work with minutes as a time unit.

```python
initial_stake = 50000000000000000000
total_period = 60000
```
### Validator Selection and Variables

We will now select a validator to delegate our tokens. We will do this by analyzing which one has the lowest `commission` and a reasonable amount of stake delegated compared to the total stake.

```python
from cosmpy.protos.cosmos.staking.v1beta1.query_pb2 import QueryValidatorsRequest

req = QueryValidatorsRequest()
resp = ledger.staking.Validators(req)

# Calculate the total stake currently in the testnet
# Status = 3 means that the validator is bonded
validators_stake = [int(validator.tokens) for validator in resp.validators if validator.status == 3]
total_stake = sum(validators_stake)

# For every bonded validator, we print comssion and percentage of total stake
print("MONIKER      COMISSION   % of TOTAL STAKE")
for validator in resp.validators:
    if validator.status == 3:
        moniker = validator.description.moniker
        comission = int(validator.commission.commission_rates.rate)/1e18*100
        print(moniker[:10]," ", comission,"%     ", round(int(validator.tokens)/total_stake*100,3),"%")
```

After running the code above, you will observe each validator commission rate and its percentage delegated of the total stake. The most important parameter to observe in each validator is the commission it will take from the rewards. We will always select a validator with the lower commission as long as it has a reasonable stake compared with the total stake. In this case, at the moment the code was run, all validators had the same commission, therefore, we simply selected the validator with the highest stake, which was validator0. Feel free to select the most convenient validator when you run the code above. We will save the variables `commission` and the fraction of our `initial_stake` to the total stake to use them later on.


```python
# get all the active validators on the network
validators = ledger.query_validators()

# Query info of selected validator
selected_validator = "validator0"
validator = [v for v in validators if v.moniker == selected_validator][0]
query_validator = [v for v in resp.validators if v.description.moniker == selected_validator][0]

# Set the comission %
commission = int(query_validator.commission.commission_rates.rate)/1e18

# Set percentage delegated of total stake
pct_delegated = initial_stake/total_stake
```

### Estimate Transaction Fees
We need to know an estimate of the transaction fees it will cost every time we claim rewards and delegate tokens. For that, both claim rewards and delegate tokens transactions were combined into a single multi-msg transaction to simulate the total fees.

```python
from cosmpy.aerial.client.distribution import create_withdraw_delegator_reward
from cosmpy.aerial.client.staking import create_delegate_msg
from cosmpy.aerial.tx import SigningCfg
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.crypto.address import Address
from cosmpy.aerial.tx import Transaction

# Use any address with at least the amount of initial_stake available
key = PrivateKey("XZ5BZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV7=")
alice = LocalWallet(key)
alice_address = Address(key)._display

tx = Transaction()

# Add delegate msg
tx.add_message(create_delegate_msg(alice_address,validator.address,initial_stake,"atestfet"))

# Add claim reward msg
tx.add_message(create_withdraw_delegator_reward(alice_address, validator.address))

account = ledger.query_account(alice.address())
tx.seal(SigningCfg.direct(alice.public_key(), account.sequence),fee="",gas_limit=0)
tx.sign(alice.signer(), ledger.network_config.chain_id, account.number)
tx.complete()

# simulate the fee for the transaction
_, str_tx_fee = ledger.estimate_gas_and_fee_for_tx(tx)
```
Since the output of this function is a string, we will convert it to an int and round it up to get a more conservative estimate for the `fee`

```python
denom = "atestfet"
tx_fee = str_tx_fee[:-len(denom)]

# Add a 20% to the fee estimation to get a more conservative estimate
fee = int(tx_fee) * 1.20
```
### Query Network Variables
There are three network variables that we need to query since they will contribute to the staking rewards calculation: `total_supply`, `inflation` and `community_tax`

```python
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
```

## Calculate Reward Rate

We can now proceed to calculate a theoretical staking rewards rate using the variables gathered above. These are: `inflation`, `total_supply`, `pct_delegated`, `community_tax` and `commission`

```python

# Calculate anual reward
anual_reward = (inflation * total_supply) *pct_delegated* (1- community_tax)*(1- commission)

# Convert from anual reward to minute reward
minute_reward = anual_reward/360/24/60

# Set the rate
rate = minute_reward/initial_stake
```

## Calculate Optimal Compounding Period

We can calculate the optimal compounding period that maximizes our staking rewards analytically by using the following formula.


<img src="../images/reward_equation.png" width="400">

Where:

*M*  = Total stake at time *D*

*S*= Initial Stake \
*f* = Transaction Fee \
*k* = Reward Rate

*m* = Number Of Compounding Transactions \
*n* = Compounding Period

*D* = *m x n* = Total Staking Time

We will now find the value that maximizes reward by taking the first derivative with respect to *n* and finding the root in the interval *(0,D]*

```python
import numpy as np
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import *
from scipy.optimize import brentq

f = fee
S = initial_stake
k = rate
D = total_period

# x will represent n
x = Symbol("x")

# Define the function
M = (S*(1+(k*x))**(D/x))+((1-((1+(k*x))**(D/x)))/(k*x))*f
Mx = lambdify(x,M)

# Take the first derivatve with repect to x
M_prime = M.diff(x)
Mx_prime = lambdify(x,M_prime)

# Find the maximum reward value by finding the root of the function
optimal_period = brentq(Mx_prime, 0.1, D)

print("optimal_period: ", analytical_optimal_period, " minutes")
```
You can make use of the `optimal_period` value in the [`staking auto-compounder`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_compounder.py) to maximize your rewards

You can also plot the function along with the optimal period to observe the results

```python
import matplotlib.pyplot as plt

plot = plt.figure(0,figsize=(6,4), dpi=100)

y = np.linspace(1,300, 100)
plt.plot(y,Mx(y),"k", label = 'analytical function')
plt.axvline(x = optimal_period, color = 'g', linewidth = 2, label = f'optimal period: {round(optimal_period)}')
plt.legend()

plt.xlabel("Compounding periods")
plt.ylabel('Total Reward')
plt.title('Maximizing Rewards')
plt.grid()
```

<img src="../images/maximizing_rewards.png" width="400">


Finally we can compare the compounding staking rewards to a simple non-compounding strategy

```python
# Compounding Strategy
comp_rewards = []
rewards = 0
period = optimal_period
S = initial_stake
for i in range(total_period):
    rewards = rewards + (S*rate)
    if i%period == 0:
        S = S + rewards - fee
        rewards = 0
    comp_rewards.append(S)
S = S + rewards - (fee/2)
comp_rewards.append(S)

# Simple Strategy
s_reward = initial_stake*rate
simple_rewards = [initial_stake+(s_reward*i) for i in range(comp_period)]

# Plots
plot = plt.figure(0,figsize=(12,4), dpi=100)

plt.subplot(1,2,1)
plt.plot(comp_rewards, label = "Compounded Rewards")
plt.plot(simple_rewards, label = "Simple Rewards")
plt.xlabel("time in minutes")
plt.ylabel('Reward')
plt.title('Staking Rewards')
plt.legend()

plt.subplot(1,2,2)

plt.plot(total_rewards, label = "Compounded Rewards")
plt.plot(simple_rewards, label = "Simple Rewards")
plt.xlabel("time in minutes")
plt.ylabel('Reward')
plt.title('Staking Rewards (log scale)')
plt.legend()

plt.yscale('log')
```
<img src="../images/compounded_vs_simple.png" width="800"> 

You can view an abbreviated version of the code at [`stake optimizer`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_stake_optimizer.py)