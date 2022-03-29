# ️Querying balance

To query the balance of an account using a [`LedgerClient`](connect-to-network.md) object `ledger_client`:

```python
balance = ledger_client.query_bank_balance('fetch1h2l3cnu7e23whmd5yrfeunacez9tv0plv5rxqy')
```

`fetch1h2l3cnu7e23whmd5yrfeunacez9tv0plv5rxqy` in the above code is the account's address.

By default, this will query the fee denomination that is in the network config associated with `ledger_client`. To explicitly specify the denomination value:

```python
balance = ledger_client.query_bank_balance('cosmos1h2l3cnu7e23whmd5yrfeunacez9tv0plv5rxqy', denom='uatom')
```