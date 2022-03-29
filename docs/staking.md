# Staking

A big part of cosmos networks is staking. Staking is the process where you can delegate your tokens to the network
validators in order to secure the network. There are three main actions you can take when staking

* **Delegating** - This is the process where you send your tokens to a chosen validator. They are applied immediately 
                   and you start earnings rewards as soon as this completes. The more that you stake, the more rewards
                   you earn.
* **Redelegating** - This is the process where you transfer your staked tokens from one validator to another. This can
                     be for many reasons like better returns, more trustworthiness etc.
* **Undelegating** - While your tokens are staked, you can not spend them or send them to other users. To regain access
                     to them, you must undelegate them. When you initiate this process the funds will be removed from
                     the validator they were delegated and must be left to cool down for a period of time (typically 21
                     days). After this period, the funds are automatically released into the user's wallet.

## Actions

### Delegate

In a similar way to [Sending Tokens](send-tokens.md), the `LedgerClient` object provides useful utilities for
interacting with the staking components of the network.

The following example illustrates a user send `20` tokens to be staked with the specified validator.

!!! note 
    For simplicity you will notice that the staking methods do not have an option for the user to specify the value for
    the `denom` field. For almost all networks there is only one staking denomination therefore the denomination is
    taken from the [`NetworkConfig`](connect-to-network.md) that was specified when creating the `LedgerClient` object

```python
validator_address = 'fetchvaloper1e4ykjwcwhwtasqxq50d4m7xz9hh7a86e9y8h87'

tx = ledger_client.delegate_tokens(validator_address, 20, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

### Redelegate

When wanting to redelegate funds from an existing validator to another validator this can be achieved with the following
code. In this example `10` tokens are transferred to `alternate_validator_address`.

```python
alternate_validator_address = 'fetchvaloper1e4ykjwcwhwtasqxq50d4m7xz9hh7a86e9y8h87'

tx = ledger_client.redelegate_tokens(validator_address, alternate_validator_address, 10, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

### Undelegate

Finally, undelegating your tokens and starting the cool down process can be done with the code below. In this example `5`
tokens are undelegated.

```python
tx = ledger_client.undelegate_tokens(validator_address, 5, wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

!!! note
    The cooldown is tracked for each invocation of undelegate action. Therefore, if you trigger 3 sets of undelegate actions
    on 3 consecutive days. The first tranche of tokens will become available 3 days before the final tranche.

### Claiming Rewards

While your funds are staked, you are earning rewards on them. Rewards can be collected at any time and unlike delegations,
when collected become immediately available for spending.

The following code illustrated how to claim rewards from a specific validator 

```python
tx = ledger_client.ledger.claim_rewards(validator_address, alice)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```

## Queries 

### Stake Summary

It is common that you will want to query the stake information for a particular address. The `LedgerClient` provides a
high level API to aggregate all the staking information for a particular address. This is shown in the example below.

```python
address = 'fetch1h2l3cnu7e23whmd5yrfeunacez9tv0plv5rxqy'

s = ledger_client.query_staking_summary(address)
print(f"Summary: Staked: {s.total_staked} Unbonding: {s.total_unbonding} Rewards: {s.total_rewards}")
```
