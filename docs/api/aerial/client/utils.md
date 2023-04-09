<a id="c4epy.aerial.client.utils"></a>

# c4epy.aerial.client.utils

Helper functions.

<a id="c4epy.aerial.client.utils.prepare_and_broadcast_basic_transaction"></a>

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

<a id="c4epy.aerial.client.utils.ensure_timedelta"></a>

#### ensure`_`timedelta

```python
def ensure_timedelta(interval: Union[int, float, timedelta]) -> timedelta
```

Return timedelta for interval.

**Arguments**:

- `interval`: timedelta or seconds in int or float

**Returns**:

timedelta

<a id="c4epy.aerial.client.utils.get_paginated"></a>

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

