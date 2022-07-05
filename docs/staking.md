A big part of the cosmos networks is staking. Staking is the process where you delegate your tokens to the network's validators in order to secure the network. There are three main actions you can take when staking:

* **Delegating**: This is the process where you send your tokens to a chosen validator. They are applied immediately and you start earning rewards as soon as this transaction completes. The more tokens you stake, the more rewards you will earn.
* **Redelegating**: This is the process where you transfer your staked tokens from one validator to another. This can be for many reasons, such as better returns, more trustworthiness, etc.
* **Undelegating**: While your tokens are staked, you cannot spend them or send them to other users. To regain access to them, you must undelegate them. When you initiate this process, the funds will be removed from the validator they were delegated to, and must be left to cool down for a period of time (for example 21 days). After this period, the funds are automatically released into the user's wallet.

## Actions

`LedgerClient` provides useful utilities for interacting with the staking component of the network.

!!! note
    For simplicity, the staking methods do not have an option for specifying the `denom` field. This is because in almost all networks, there is only one staking denomination. Therefore, the denomination used is the one specified in the [`NetworkConfig`](connect-to-network.md) supplied to the `LedgerClient` object.

### Delegate

To stake `20` tokens with the specific validator using a [`Wallet`](wallets-and-keys.md):

```python
validator_address = 'fetchvaloper1e4ykjwcwhwtasqxq50d4m7xz9hh7a86e9y8h87'

tx = ledger_client.delegate_tokens(validator_address, 20, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

### Redelegate

To redelegate `10` tokens from an existing validator (with the address `validator_address`) to another (with the address `alternate_validator_address`):

```python
validator_address = 'fetchvaloper1e4ykjwcwhwtasqxq50d4m7xz9hh7a86e9y8h87'
alternate_validator_address = 'fetchvaloper1e4ykjwcwhwtasqxq50d4m7xz9hh7a86e9y8h87'

tx = ledger_client.redelegate_tokens(validator_address, alternate_validator_address, 10, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

### Undelegate

To undelegate `5` tokens and start the cool down process:

```python
tx = ledger_client.undelegate_tokens(validator_address, 5, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

!!! note
    The cool down is tracked for each invocation of undelegate action. So for example if you trigger 3 undelegate actions on 3 consecutive days. The first batch of tokens will become available 3 days before the final batch.

### Claiming Rewards

While your funds are staked, you are earning rewards on them. Rewards can be collected at any time and unlike delegations, when collected they become immediately available.

To claim rewards from a specific validator: 

```python
tx = ledger_client.claim_rewards(validator_address, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

## Queries

### Stake Summary

At any point you can query the stake information of any particular address. This can be done using the `LedgerClient` as shown in the example below:

```python
address = 'fetch1h2l3cnu7e23whmd5yrfeunacez9tv0plv5rxqy'

s = ledger_client.query_staking_summary(address)
print(f"Summary: Staked: {s.total_staked} Unbonding: {s.total_unbonding} Rewards: {s.total_rewards}")
```
