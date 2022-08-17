<a id="cosmpy.aerial.gas"></a>

# cosmpy.aerial.gas

Transaction gas startegy

<a id="cosmpy.aerial.gas.GasStrategy"></a>

## GasStrategy Objects

```python
class GasStrategy(ABC)
```

Transaction gas startegy

<a id="cosmpy.aerial.gas.GasStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
@abstractmethod
def estimate_gas(tx: Transaction) -> int
```

Estimate the transaction gas

**Arguments**:

- `tx`: Transaction

**Returns**:

None

<a id="cosmpy.aerial.gas.GasStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
@abstractmethod
def block_gas_limit() -> int
```

Get the block gas limit

**Returns**:

None

<a id="cosmpy.aerial.gas.SimulationGasStrategy"></a>

## SimulationGasStrategy Objects

```python
class SimulationGasStrategy(GasStrategy)
```

Simulation transaction gas startegy

**Arguments**:

- `GasStrategy`: gas strategy

<a id="cosmpy.aerial.gas.SimulationGasStrategy.__init__"></a>

#### `__`init`__`

```python
def __init__(client: "LedgerClient", multiplier: Optional[float] = None)
```

Init the Simulation transaction gas startegy

**Arguments**:

- `client`: Ledger client
- `multiplier`: multiplier, defaults to None

<a id="cosmpy.aerial.gas.SimulationGasStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
def estimate_gas(tx: Transaction) -> int
```

Get estimated transaction gas

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated transaction gas

<a id="cosmpy.aerial.gas.SimulationGasStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
def block_gas_limit() -> int
```

Get the block gas limit

**Returns**:

block gas limit

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy"></a>

## OfflineMessageTableStrategy Objects

```python
class OfflineMessageTableStrategy(GasStrategy)
```

Offline message table strategy

**Arguments**:

- `GasStrategy`: gas strategy

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy.default_table"></a>

#### default`_`table

```python
@staticmethod
def default_table() -> "OfflineMessageTableStrategy"
```

offline message strategy default table

**Returns**:

offline message default table strategy

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy.__init__"></a>

#### `__`init`__`

```python
def __init__(fallback_gas_limit: Optional[int] = None,
             block_limit: Optional[int] = None)
```

Init offline message table strategy

**Arguments**:

- `fallback_gas_limit`: Fallback gas limit, defaults to None
- `block_limit`: Block limit, defaults to None

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy.update_entry"></a>

#### update`_`entry

```python
def update_entry(transaction_type: str, gas_limit: int)
```

Udate the entry of the transaction

**Arguments**:

- `transaction_type`: transaction type
- `gas_limit`: gas limit

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy.estimate_gas"></a>

#### estimate`_`gas

```python
def estimate_gas(tx: Transaction) -> int
```

Get estimated transaction gas

**Arguments**:

- `tx`: transaction

**Returns**:

Estimated transaction gas

<a id="cosmpy.aerial.gas.OfflineMessageTableStrategy.block_gas_limit"></a>

#### block`_`gas`_`limit

```python
def block_gas_limit() -> int
```

Get the block gas limit

**Returns**:

block gas limit

