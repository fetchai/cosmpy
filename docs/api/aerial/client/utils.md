<a id="cosmpy.aerial.client.utils"></a>

# cosmpy.aerial.client.utils

Helper functions.

<a id="cosmpy.aerial.client.utils.prepare_and_broadcast_basic_transaction"></a>

#### prepare`_`and`_`broadcast`_`basic`_`transaction

```python
def prepare_and_broadcast_basic_transaction(
        client: "LedgerClient",
        tx: "Transaction",
        sender: "Wallet",
        account: Optional["Account"] = None,
        gas_limit: Optional[int] = None,
        memo: Optional[str] = None) -> SubmittedTx
```

Prepare and broadcast basic transaction.

**Arguments**:

- `client`: Ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `gas_limit`: The gas limit
- `memo`: Transaction memo, defaults to None

**Returns**:

broadcast transaction

<a id="cosmpy.aerial.client.utils.ensure_timedelta"></a>

#### ensure`_`timedelta

```python
def ensure_timedelta(interval: Union[int, float, timedelta]) -> timedelta
```

Return timedelta for interval.

**Arguments**:

- `interval`: timedelta or seconds in int or float

**Returns**:

timedelta
