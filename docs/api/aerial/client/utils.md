<a id="cosmpy.aerial.client.utils"></a>

# cosmpy.aerial.client.utils

Helper functions.

<a id="cosmpy.aerial.client.utils.simulate_tx"></a>

#### simulate`_`tx

```python
def simulate_tx(client: "LedgerClient",
                tx: Transaction,
                sender: Wallet,
                account: Optional[Account],
                memo: Optional[str] = None) -> Tuple[int, str, Account]
```

Estimate transaction fees based on either a provided amount, gas limit, or simulation.

**Arguments**:

- `client`: Ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `memo`: Transaction memo, defaults to None

**Returns**:

Estimated gas_limit and fee amount tuple

<a id="cosmpy.aerial.client.utils.prepare_basic_transaction"></a>

#### prepare`_`basic`_`transaction

```python
def prepare_basic_transaction(
        client: "LedgerClient",
        tx: Transaction,
        sender: Wallet,
        account: Optional[Account] = None,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None) -> Transaction
```

Prepare basic transaction.

**Arguments**:

- `client`: Ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `fee`: The tx fee
- `memo`: Transaction memo, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

transaction

<a id="cosmpy.aerial.client.utils.prepare_and_broadcast_basic_transaction"></a>

#### prepare`_`and`_`broadcast`_`basic`_`transaction

```python
def prepare_and_broadcast_basic_transaction(
        client: "LedgerClient",
        tx: Transaction,
        sender: Wallet,
        account: Optional[Account] = None,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None) -> SubmittedTx
```

Prepare and broadcast basic transaction.

**Arguments**:

- `client`: Ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `fee`: The tx fee
- `memo`: Transaction memo, defaults to None
- `timeout_height`: timeout height, defaults to None

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

<a id="cosmpy.aerial.client.utils.get_paginated"></a>

#### get`_`paginated

```python
def get_paginated(
        initial_request: Any,
        request_method: Callable,
        pages_limit: int = 0,
        per_page_limit: Optional[int] = DEFAULT_PER_PAGE_LIMIT) -> List[Any]
```

Get pages for specific request.

**Arguments**:

- `initial_request`: request supports pagination
- `request_method`: function to perform request
- `pages_limit`: max number of pages to return. default - 0 unlimited
- `per_page_limit`: Optional int: amount of records per one page. default is None, determined by server

**Returns**:

List of responses

