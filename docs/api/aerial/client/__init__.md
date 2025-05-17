<a id="cosmpy.aerial.client.__init__"></a>

# cosmpy.aerial.client.`__`init`__`

Client functionality.

<a id="cosmpy.aerial.client.__init__.LedgerClient"></a>

## LedgerClient Objects

```python
class LedgerClient()
```

Ledger client.

<a id="cosmpy.aerial.client.__init__.LedgerClient.__init__"></a>

#### `__`init`__`

```python
def __init__(cfg: NetworkConfig,
             query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
             query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS)
```

Init ledger client.

**Arguments**:

- `cfg`: Network configurations
- `query_interval_secs`: int. optional interval int seconds
- `query_timeout_secs`: int. optional interval int seconds

<a id="cosmpy.aerial.client.__init__.LedgerClient.network_config"></a>

#### network`_`config

```python
@property
def network_config() -> NetworkConfig
```

Get the network config.

**Returns**:

network config

<a id="cosmpy.aerial.client.__init__.LedgerClient.gas_strategy"></a>

#### gas`_`strategy

```python
@property
def gas_strategy() -> GasStrategy
```

Get gas strategy.

**Returns**:

gas strategy

<a id="cosmpy.aerial.client.__init__.LedgerClient.gas_strategy"></a>

#### gas`_`strategy

```python
@gas_strategy.setter
def gas_strategy(strategy: GasStrategy)
```

Set gas strategy.

**Arguments**:

- `strategy`: strategy

**Raises**:

- `RuntimeError`: Invalid strategy must implement GasStrategy interface

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_account"></a>

#### query`_`account

```python
def query_account(address: Address) -> Account
```

Query account.

**Arguments**:

- `address`: address

**Raises**:

- `RuntimeError`: Unexpected account type returned from query

**Returns**:

account details

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_params"></a>

#### query`_`params

```python
def query_params(subspace: str, key: str) -> Any
```

Query Prams.

**Arguments**:

- `subspace`: subspace
- `key`: key

**Returns**:

Query params

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_bank_balance"></a>

#### query`_`bank`_`balance

```python
def query_bank_balance(address: Address, denom: Optional[str] = None) -> int
```

Query bank balance.

**Arguments**:

- `address`: address
- `denom`: denom, defaults to None

**Returns**:

bank balance

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_bank_all_balances"></a>

#### query`_`bank`_`all`_`balances

```python
def query_bank_all_balances(address: Address) -> List[Coin]
```

Query bank all balances.

**Arguments**:

- `address`: address

**Returns**:

bank all balances

<a id="cosmpy.aerial.client.__init__.LedgerClient.send_tokens"></a>

#### send`_`tokens

```python
def send_tokens(destination: Address,
                amount: int,
                denom: str,
                sender: Wallet,
                memo: Optional[str] = None,
                fee: Optional[TxFee] = None,
                timeout_height: Optional[int] = None) -> SubmittedTx
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_validators"></a>

#### query`_`validators

```python
def query_validators(
        status: Optional[ValidatorStatus] = None) -> List[Validator]
```

Query validators.

**Arguments**:

- `status`: validator status, defaults to None

**Returns**:

List of validators

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_staking_summary"></a>

#### query`_`staking`_`summary

```python
def query_staking_summary(address: Address) -> StakingSummary
```

Query staking summary.

**Arguments**:

- `address`: address

**Returns**:

staking summary

<a id="cosmpy.aerial.client.__init__.LedgerClient.delegate_tokens"></a>

#### delegate`_`tokens

```python
def delegate_tokens(validator: Address,
                    amount: int,
                    sender: Wallet,
                    memo: Optional[str] = None,
                    fee: Optional[TxFee] = None,
                    timeout_height: Optional[int] = None) -> SubmittedTx
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.redelegate_tokens"></a>

#### redelegate`_`tokens

```python
def redelegate_tokens(current_validator: Address,
                      next_validator: Address,
                      amount: int,
                      sender: Wallet,
                      memo: Optional[str] = None,
                      fee: Optional[TxFee] = None,
                      timeout_height: Optional[int] = None) -> SubmittedTx
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.undelegate_tokens"></a>

#### undelegate`_`tokens

```python
def undelegate_tokens(validator: Address,
                      amount: int,
                      sender: Wallet,
                      memo: Optional[str] = None,
                      fee: Optional[TxFee] = None,
                      timeout_height: Optional[int] = None) -> SubmittedTx
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.claim_rewards"></a>

#### claim`_`rewards

```python
def claim_rewards(validator: Address,
                  sender: Wallet,
                  memo: Optional[str] = None,
                  fee: Optional[TxFee] = None,
                  timeout_height: Optional[int] = None) -> SubmittedTx
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.estimate_gas_for_tx"></a>

#### estimate`_`gas`_`for`_`tx

```python
def estimate_gas_for_tx(tx: Transaction) -> int
```

Estimate gas for transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated gas for transaction

<a id="cosmpy.aerial.client.__init__.LedgerClient.estimate_fee_from_gas"></a>

#### estimate`_`fee`_`from`_`gas

```python
def estimate_fee_from_gas(gas_limit: int) -> str
```

Estimate fee from gas.

**Arguments**:

- `gas_limit`: gas limit

**Returns**:

Estimated fee for transaction

<a id="cosmpy.aerial.client.__init__.LedgerClient.estimate_gas_and_fee_for_tx"></a>

#### estimate`_`gas`_`and`_`fee`_`for`_`tx

```python
def estimate_gas_and_fee_for_tx(tx: Transaction) -> Tuple[int, str]
```

Estimate gas and fee for transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

estimate gas, fee for transaction

<a id="cosmpy.aerial.client.__init__.LedgerClient.wait_for_query_tx"></a>

#### wait`_`for`_`query`_`tx

```python
def wait_for_query_tx(tx_hash: str,
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

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_tx"></a>

#### query`_`tx

```python
def query_tx(tx_hash: str) -> TxResponse
```

query transaction.

**Arguments**:

- `tx_hash`: transaction hash

**Raises**:

- `NotFoundError`: Tx details not found
- `grpc.RpcError`: RPC connection issue

**Returns**:

query response

<a id="cosmpy.aerial.client.__init__.LedgerClient.simulate_tx"></a>

#### simulate`_`tx

```python
def simulate_tx(tx: Transaction) -> int
```

simulate transaction.

**Arguments**:

- `tx`: transaction

**Raises**:

- `RuntimeError`: Unable to simulate non final transaction

**Returns**:

gas used in transaction

<a id="cosmpy.aerial.client.__init__.LedgerClient.broadcast_tx"></a>

#### broadcast`_`tx

```python
def broadcast_tx(tx: Transaction) -> SubmittedTx
```

Broadcast transaction.

**Arguments**:

- `tx`: transaction

**Returns**:

Submitted transaction

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_latest_block"></a>

#### query`_`latest`_`block

```python
def query_latest_block() -> Block
```

Query the latest block.

**Returns**:

latest block

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_block"></a>

#### query`_`block

```python
def query_block(height: int) -> Block
```

Query the block.

**Arguments**:

- `height`: block height

**Returns**:

block

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_height"></a>

#### query`_`height

```python
def query_height() -> int
```

Query the latest block height.

**Returns**:

latest block height

<a id="cosmpy.aerial.client.__init__.LedgerClient.query_chain_id"></a>

#### query`_`chain`_`id

```python
def query_chain_id() -> str
```

Query the chain id.

**Returns**:

chain id

