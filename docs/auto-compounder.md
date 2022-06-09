When an account delegates tokens to a network's validator, it will start generating rewards proportional to the amount of [`Stake`](staking.md) delegated. But since rewards aren't automatically added to your stake and therefore don't contribute to future rewards, we can perform a compounding strategy to generate exponential rewards.

## Delegate

The first thing we need to do is delegate some tokens to a `validator`. You can do so by using a [`Wallet`](wallets-and-keys.md) and specifying the validator address and amount.

```python
validators = ledger_client.query_validators()

# choose any validator
validator = validators[0]

key = PrivateKey("FX5BZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV7=")
wallet = LocalWallet(key)

# delegate some tokens to this validator
tx = ledger_client.delegate_tokens(validator.address, 9000000000000000000, wallet)
tx.wait_to_complete()
```

## Auto Compounder

Then we can construct a code that claims rewards and delegates the rewarded tokens back to the `validator`. This way we keep growing our [`Stake`](staking.md) and therefore we generate compounded rewards. We first need to define the `time limit` and the compounding `period`.

It is important to note that each time an account performs a claim or a delegate transaction it has to pay certain fees, therefore the compounding period has to be long enough to generate sufficient rewards to exceed the fees that will be paid in each transaction.

```python
# set time limit and compounding period in seconds
time_limit = 600
period = 100
```
Finally, we start a timer that claims rewards and delegates them in each time period. Notice that in the code below we constructed a while loop that will be running until the timer exceeds the `time limit`. Each loop will last the time specified in `period`. We query the balance before and after claiming rewards to get the value of the reward after any fees. If the true reward value is positive, we delegate those tokens to the validator, if it is negative, it means that the fees from claiming and delegating transactions exceeded the rewards and therefore we won't delegate.


```python
time_check = 0
start_time = time.monotonic()
time.sleep(period)

# query, claim and delegate rewards after time period
while time_check < time_limit:
    
    begin = time.monotonic()

    summary = ledger_client.query_staking_summary(wallet.address())
    print(f"Staked: {summary.total_staked}")

    balance_before = ledger_client.query_bank_balance(wallet.address())

    tx = ledger_client.claim_rewards(validator.address, wallet)
    tx.wait_to_complete()

    balance_after = ledger_client.query_bank_balance(wallet.address())

    # reward after any fees
    true_reward = balance_after - balance_before

    if true_reward > 0:

        print(f"Staking {true_reward} (reward after fees)")

        tx = ledger_client.delegate_tokens(validator.address, true_reward, wallet)
        tx.wait_to_complete()

    else:
        print("Fees from claim rewards transaction exceeded reward")
    
    end = time.monotonic()

    time.sleep(period-(end-begin))
    time_check = time.monotonic() - start_time
```

You can view the full python example at [staking auto-compounder](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_compounder.py)