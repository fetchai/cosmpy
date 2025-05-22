<a id="cosmpy.aerial.coins"></a>

# cosmpy.aerial.coins

Parse the coins.

<a id="cosmpy.aerial.coins.parse_coins"></a>

#### parse`_`coins

```python
def parse_coins(value: str) -> List[Coin]
```

Parse the coins.

**Arguments**:

- `value`: coins

**Raises**:

- `RuntimeError`: If unable to parse the value

**Returns**:

coins

<a id="cosmpy.aerial.coins.to_coins"></a>

#### to`_`coins

```python
def to_coins(amount: CoinsParamType) -> List[Coin]
```

Convert various fee amount formats into a standardized list of Coin objects.

Accepts a string in standard Cosmos coin notation (e.g., "100uatom,200afet"), or a single Coin,
or a list of Coins and returns a corresponding list of Coin instances.

**Arguments**:

- `amount`: A string representing one or more coins, Coin, or a list of Coin objects.

**Raises**:

- `TypeError`: If the input is not a supported type.

**Returns**:

A list of Coin objects.

