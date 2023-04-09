<a id="c4epy.aerial.gas"></a>

# c4epy.aerial.gas

Transaction gas strategy.

<a id="c4epy.aerial.gas.GasStrategy"></a>

## GasStrategy Objects

```python
class GasStrategy(ABC)
```

Transaction gas strategy.

<a id="c4epy.aerial.gas.GasStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
@abstractmethod
def estimate_gas(tx: Transaction) -> int
```

Estimate the transaction gas.

**Arguments**:

- `tx`: Transaction

**Returns**:

None

<a id="c4epy.aerial.gas.GasStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
@abstractmethod
def block_gas_limit() -> int
```

Get the block gas limit.

**Returns**:

None

<a id="c4epy.aerial.gas.SimulationGasStrategy"></a>

## SimulationGasStrategy Objects

```python
class SimulationGasStrategy(GasStrategy)
```

Simulation transaction gas strategy.

**Arguments**:

- `GasStrategy`: gas strategy

<a id="c4epy.aerial.gas.SimulationGasStrategy.__init__"></a>

#### `__`init`__`

```python
def __init__(client: "LedgerClient", multiplier: Optional[float] = None)
```

Init the Simulation transaction gas strategy.

**Arguments**:

- `client`: Ledger client
- `multiplier`: multiplier, defaults to None

<a id="c4epy.aerial.gas.SimulationGasStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
def estimate_gas(tx: Transaction) -> int
```

Get estimated transaction gas.

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated transaction gas

<a id="c4epy.aerial.gas.SimulationGasStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
def block_gas_limit() -> int
```

Get the block gas limit.

**Returns**:

block gas limit

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy"></a>

## OfflineMessageTableStrategy Objects

```python
class OfflineMessageTableStrategy(GasStrategy)
```

Offline message table strategy.

**Arguments**:

- `GasStrategy`: gas strategy

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy.default_table"></a>

#### default`_`table

```python
@staticmethod
def default_table() -> "OfflineMessageTableStrategy"
```

offline message strategy default table.

**Returns**:

offline message default table strategy

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy.__init__"></a>

#### `__`init`__`

```python
def __init__(fallback_gas_limit: Optional[int] = None,
             block_limit: Optional[int] = None)
```

Init offline message table strategy.

**Arguments**:

- `fallback_gas_limit`: Fallback gas limit, defaults to None
- `block_limit`: Block limit, defaults to None

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy.update_entry"></a>

#### update`_`entry

```python
def update_entry(transaction_type: str, gas_limit: int)
```

Update the entry of the transaction.

**Arguments**:

- `transaction_type`: transaction type
- `gas_limit`: gas limit

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
def estimate_gas(tx: Transaction) -> int
```

Get estimated transaction gas.

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated transaction gas

<a id="c4epy.aerial.gas.OfflineMessageTableStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
def block_gas_limit() -> int
```

Get the block gas limit.

**Returns**:

block gas limit

