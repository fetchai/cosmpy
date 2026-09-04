<a id="cosmpy.aerial.client.aio"></a>

# cosmpy.aerial.client.aio

Asyncio-native client functionality (gRPC endpoints only).

``AsyncLedgerClient`` mirrors ``LedgerClient`` method for method, but performs
all network I/O on grpc's native asyncio channel (``grpc.aio``) — no worker
threads involved. It reuses the same generated protobuf stubs as the sync
client; the stubs return awaitables when constructed over an aio channel.

Note: instantiate the client from within a running event loop (i.e. inside the
coroutine passed to ``asyncio.run``) — the underlying grpc.aio channel binds to
the running loop when it is created.

Usage:

.. code-block:: python

async with AsyncLedgerClient(NetworkConfig.fetchai_mainnet()) as client:
balance = await client.query_bank_balance(address)

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient"></a>

## AsyncLedgerClient Objects

```python
class AsyncLedgerClient(LedgerClientBase)
```

Asyncio-native ledger client (gRPC endpoints only).

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.__init__"></a>

#### `__`init`__`

```python
def __init__(cfg: NetworkConfig,
             query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
             query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS)
```

Init async ledger client.

**Arguments**:

- `cfg`: Network configurations
- `query_interval_secs`: int. optional interval int seconds
- `query_timeout_secs`: int. optional interval int seconds

**Raises**:

- `RuntimeError`: Network config url is not a gRPC endpoint

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.close"></a>

#### close

```python
async def close()
```

Close the underlying gRPC channel.

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.__aenter__"></a>

#### `__`aenter`__`

```python
async def __aenter__() -> "AsyncLedgerClient"
```

Enter the async context.

**Returns**:

this client

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.__aexit__"></a>

#### `__`aexit`__`

```python
async def __aexit__(exc_type, exc_value, traceback)
```

Exit the async context, closing the gRPC channel.

**Arguments**:

- `exc_type`: exception type
- `exc_value`: exception value
- `traceback`: exception traceback

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.gas_strategy"></a>

#### gas`_`strategy

```python
@property
def gas_strategy() -> Union[GasStrategy, AsyncGasStrategy]
```

Get gas strategy.

**Returns**:

gas strategy

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.gas_strategy"></a>

#### gas`_`strategy

```python
@gas_strategy.setter
def gas_strategy(strategy: Union[GasStrategy, AsyncGasStrategy])
```

Set gas strategy.

**Arguments**:

- `strategy`: strategy

**Raises**:

- `RuntimeError`: Invalid strategy must implement GasStrategy or AsyncGasStrategy interface

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_account"></a>

#### query`_`account

```python
async def query_account(address: Address) -> Account
```

Query account.

**Arguments**:

- `address`: address

**Returns**:

account details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_params"></a>

#### query`_`params

```python
async def query_params(subspace: str, key: str) -> Any
```

Query Prams.

**Arguments**:

- `subspace`: subspace
- `key`: key

**Returns**:

Query params

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_node_info"></a>

#### query`_`node`_`info

```python
async def query_node_info() -> NodeInfo
```

Query basic Tendermint / node information (moniker, chain-id, version, etc.).

**Returns**:

NodeInfo.

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_consensus_params"></a>

#### query`_`consensus`_`params

```python
async def query_consensus_params() -> Any
```

Query consensus params.

**Returns**:

Query consensus params

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_bank_balance"></a>

#### query`_`bank`_`balance

```python
async def query_bank_balance(address: Address,
                             denom: Optional[str] = None) -> int
```

Query bank balance.

**Arguments**:

- `address`: address
- `denom`: denom, defaults to None

**Returns**:

bank balance

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_bank_all_balances"></a>

#### query`_`bank`_`all`_`balances

```python
async def query_bank_all_balances(address: Address) -> List[Coin]
```

Query bank all balances.

**Arguments**:

- `address`: address

**Returns**:

bank all balances

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.send_tokens"></a>

#### send`_`tokens

```python
async def send_tokens(
        destination: Address,
        amount: int,
        denom: str,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

Send tokens.

**Arguments**:

- `destination`: destination address
- `amount`: amount
- `denom`: denom
- `sender`: sender
- `memo`: memo, defaults to None
- `fee`: transaction fee, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

prepare and broadcast the transaction and transaction details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_validators"></a>

#### query`_`validators

```python
async def query_validators(
        status: Optional[ValidatorStatus] = None) -> List[Validator]
```

Query validators.

**Arguments**:

- `status`: validator status, defaults to None

**Returns**:

List of validators

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_staking_summary"></a>

#### query`_`staking`_`summary

```python
async def query_staking_summary(address: Address) -> StakingSummary
```

Query staking summary.

**Arguments**:

- `address`: address

**Returns**:

staking summary

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.delegate_tokens"></a>

#### delegate`_`tokens

```python
async def delegate_tokens(
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

Delegate tokens.

**Arguments**:

- `validator`: validator address
- `amount`: amount
- `sender`: sender
- `memo`: memo, defaults to None
- `fee`: transaction fee, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

prepare and broadcast the transaction and transaction details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.redelegate_tokens"></a>

#### redelegate`_`tokens

```python
async def redelegate_tokens(
        current_validator: Address,
        next_validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

Redelegate tokens.

**Arguments**:

- `current_validator`: current validator address
- `next_validator`: next validator address
- `amount`: amount
- `sender`: sender
- `memo`: memo, defaults to None
- `fee`: transaction fee, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

prepare and broadcast the transaction and transaction details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.undelegate_tokens"></a>

#### undelegate`_`tokens

```python
async def undelegate_tokens(
        validator: Address,
        amount: int,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

Undelegate tokens.

**Arguments**:

- `validator`: validator
- `amount`: amount
- `sender`: sender
- `memo`: memo, defaults to None
- `fee`: transaction fee, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

prepare and broadcast the transaction and transaction details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.claim_rewards"></a>

#### claim`_`rewards

```python
async def claim_rewards(
        validator: Address,
        sender: Wallet,
        memo: Optional[str] = None,
        fee: Optional[TxFee] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

claim rewards.

**Arguments**:

- `validator`: validator
- `sender`: sender
- `memo`: memo, defaults to None
- `fee`: transaction fee, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

prepare and broadcast the transaction and transaction details

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.estimate_gas_for_tx"></a>

#### estimate`_`gas`_`for`_`tx

```python
async def estimate_gas_for_tx(tx: Transaction) -> int
```

Estimate gas for transaction.

Supports both async and (I/O-free) sync gas strategies.

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated gas for transaction

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.estimate_gas_and_fee_for_tx"></a>

#### estimate`_`gas`_`and`_`fee`_`for`_`tx

```python
async def estimate_gas_and_fee_for_tx(tx: Transaction) -> Tuple[int, str]
```

Estimate gas and fee for transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

estimate gas, fee for transaction

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.wait_for_query_tx"></a>

#### wait`_`for`_`query`_`tx

```python
async def wait_for_query_tx(
        tx_hash: str,
        timeout: Optional[timedelta] = None,
        poll_period: Optional[timedelta] = None) -> TxResponse
```

Wait for query transaction.

**Arguments**:

- `tx_hash`: transaction hash
- `timeout`: timeout, defaults to None
- `poll_period`: poll_period, defaults to None

**Raises**:

- `QueryTimeoutError`: timeout

**Returns**:

transaction response

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_tx"></a>

#### query`_`tx

```python
async def query_tx(tx_hash: str) -> TxResponse
```

query transaction.

**Arguments**:

- `tx_hash`: transaction hash

**Raises**:

- `NotFoundError`: Tx details not found
- `grpc.RpcError`: RPC connection issue

**Returns**:

query response

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.simulate_tx"></a>

#### simulate`_`tx

```python
async def simulate_tx(tx: Transaction) -> int
```

simulate transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

gas used in transaction

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.broadcast_tx"></a>

#### broadcast`_`tx

```python
async def broadcast_tx(tx: Transaction) -> AsyncSubmittedTx
```

Broadcast transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

Submitted transaction

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_latest_block"></a>

#### query`_`latest`_`block

```python
async def query_latest_block() -> Block
```

Query the latest block.

**Returns**:

latest block

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_block"></a>

#### query`_`block

```python
async def query_block(height: int) -> Block
```

Query the block.

**Arguments**:

- `height`: block height

**Returns**:

block

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_height"></a>

#### query`_`height

```python
async def query_height() -> int
```

Query the latest block height.

**Returns**:

latest block height

<a id="cosmpy.aerial.client.aio.AsyncLedgerClient.query_chain_id"></a>

#### query`_`chain`_`id

```python
async def query_chain_id() -> str
```

Query the chain id.

**Returns**:

chain id

<a id="cosmpy.aerial.client.aio.simulate_tx"></a>

#### simulate`_`tx

```python
async def simulate_tx(client: AsyncLedgerClient,
                      tx: Transaction,
                      sender: Wallet,
                      account: Optional[Account] = None,
                      memo: Optional[str] = None) -> Tuple[int, str, Account]
```

Estimate transaction fees based on either a provided amount, gas limit, or simulation.

**Arguments**:

- `client`: Async ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `memo`: Transaction memo, defaults to None

**Returns**:

Estimated gas_limit and fee amount tuple

<a id="cosmpy.aerial.client.aio.prepare_basic_transaction"></a>

#### prepare`_`basic`_`transaction

```python
async def prepare_basic_transaction(
        client: AsyncLedgerClient,
        tx: Transaction,
        sender: Wallet,
        account: Optional[Account] = None,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None) -> Transaction
```

Prepare basic transaction.

**Arguments**:

- `client`: Async ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `fee`: The tx fee (see below the behaviour):
- If the `fee` *or* `fee.gas_limit` is `None`, then the `simulate_tx(...)` will be executed to
  estimate the `fee.gas_limit` value.
- If the `fee.amount` is `None` then it will be calculated from the `fee.gas_limit` and `gas_price`
  values (the `gas_price` value will be taken from client config).
- `memo`: Transaction memo, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

transaction

<a id="cosmpy.aerial.client.aio.prepare_and_broadcast_basic_transaction"></a>

#### prepare`_`and`_`broadcast`_`basic`_`transaction

```python
async def prepare_and_broadcast_basic_transaction(
        client: AsyncLedgerClient,
        tx: Transaction,
        sender: Wallet,
        account: Optional[Account] = None,
        fee: Optional[TxFee] = None,
        memo: Optional[str] = None,
        timeout_height: Optional[int] = None) -> AsyncSubmittedTx
```

Prepare and broadcast basic transaction.

**Arguments**:

- `client`: Async ledger client
- `tx`: The transaction
- `sender`: The transaction sender
- `account`: The account
- `fee`: The tx fee (see below the behaviour):
- If the `fee` *or* `fee.gas_limit` is `None`, then the `simulate_tx(...)` will be executed to
  estimate the `fee.gas_limit` value.
- If the `fee.amount` is `None` then it will be calculated from the `fee.gas_limit` and `gas_price`
  values (the `gas_price` value will be taken from client config).
- `memo`: Transaction memo, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

broadcast transaction

<a id="cosmpy.aerial.client.aio.get_paginated"></a>

#### get`_`paginated

```python
async def get_paginated(
        initial_request: Any,
        request_method: Callable,
        pages_limit: int = 0,
        per_page_limit: Optional[int] = DEFAULT_PER_PAGE_LIMIT) -> List[Any]
```

Get pages for specific request.

**Arguments**:

- `initial_request`: request supports pagination
- `request_method`: async function to perform request
- `pages_limit`: max number of pages to return. default - 0 unlimited
- `per_page_limit`: Optional int: amount of records per one page. default is None, determined by server

**Returns**:

List of responses

