Once you have your [`wallet`](wallets-and-keys.md) configured, you can send transactions to the network. The `LedgerClient` object provides useful utilities to do common operations. The following example shows how to send `10` `atestasi` to another address:

```python
destination_address = 'asi1h2l3cnu7e23whmd5yrfeunacez9tv0plhkcjz8'

tx = ledger_client.send_tokens(destination_address, 10, "atestasi", wallet)

# block until the transaction has been successful or failed
tx.wait_to_complete()
```
