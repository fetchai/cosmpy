<a id="cosmpy.aerial.coins"></a>

# cosmpy.aerial.coins

Parse the coins.

<a id="cosmpy.aerial.coins.Coin"></a>

## Coin Objects

```python
@dataclass
class Coin()
```

Coins.

<a id="cosmpy.aerial.coins.Coin.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> CoinProto
```

Convert this type to protobuf schema Coin type.

<a id="cosmpy.aerial.coins.Coin.__repr__"></a>

#### `__`repr`__`

```python
def __repr__() -> str
```

Return string representation of coin.

<a id="cosmpy.aerial.coins.Coin.validate"></a>

#### validate

```python
def validate()
```

Validate this type based on Cosmos-SDK requirements for Coin.

<a id="cosmpy.aerial.coins.Coins"></a>

## Coins Objects

```python
class Coins(List[Coin])
```

Coins.

<a id="cosmpy.aerial.coins.Coins.__init__"></a>

#### `__`init`__`

```python
def __init__(coins: Optional[Union[str, "Coins", List[Coin], List[CoinProto],
                                   Coin, CoinProto]] = None)
```

Convert any coin representation into normalised Coins.

<a id="cosmpy.aerial.coins.Coins.__repr__"></a>

#### `__`repr`__`

```python
def __repr__() -> str
```

Return string representation of Coins.

<a id="cosmpy.aerial.coins.Coins.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> List[CoinProto]
```

Convert this type to protobuf schema Coins type.

<a id="cosmpy.aerial.coins.Coins.canonicalise"></a>

#### canonicalise

```python
def canonicalise()
```

Reorganise the value of the instance (list of coins) in to canonical form defined by cosmos-sdk for `Coins`.

This means alphabetically sorting (descending) the coins based on denomination.
The algorithm *fails* with exception *if* each denomination in the list is *not* unique = if some denominations
are present in the coin list more than once.

<a id="cosmpy.aerial.coins.Coins.validate"></a>

#### validate

```python
def validate()
```

Validate whether current value conforms to canonical form for list of coins defined by cosmos-sdk.

<a id="cosmpy.aerial.coins.Coins.__add__"></a>

#### `__`add`__`

```python
def __add__(other)
```

Perform algebraic vector addition of two coin lists.

<a id="cosmpy.aerial.coins.Coins.__sub__"></a>

#### `__`sub`__`

```python
def __sub__(other)
```

Perform algebraic vector substraction of two coin lists, ensuring no coin has negative value.

<a id="cosmpy.aerial.coins.Coins.__iadd__"></a>

#### `__`iadd`__`

```python
def __iadd__(other)
```

Perform *in-place* algebraic vector substraction of two coin lists.

<a id="cosmpy.aerial.coins.Coins.__isub__"></a>

#### `__`isub`__`

```python
def __isub__(other)
```

Perform *in-place* algebraic vector substraction of two coin lists, ensuring no coin has negative value.

<a id="cosmpy.aerial.coins.parse_coins"></a>

#### parse`_`coins

```python
def parse_coins(value: str) -> List[CoinProto]
```

Parse the coins.

**Arguments**:

- `value`: coins encoded in cosmos-sdk string format

**Returns**:

List of CoinProto objects

<a id="cosmpy.aerial.coins.is_denom_valid"></a>

#### is`_`denom`_`valid

```python
def is_denom_valid(denom: str) -> bool
```

Return true if coin denom name is valid.

**Arguments**:

- `denom`: string denom

**Returns**:

bool validity

<a id="cosmpy.aerial.coins.is_coins_sorted"></a>

#### is`_`coins`_`sorted

```python
def is_coins_sorted(
        coins: Union[str, Coins, List[Coin], List[CoinProto]]) -> bool
```

Return true if given coins representation is sorted.

**Arguments**:

- `coins`: Any type representing coins

**Returns**:

bool is_sorted

<a id="cosmpy.aerial.coins.validate_coins"></a>

#### validate`_`coins

```python
def validate_coins(coins: Union[str, Coins, List[Coin], List[CoinProto]])
```

Return true if given coins representation is valid.

**Arguments**:

- `coins`: Any type representing coins

**Raises**:

- `ValueError`: If there are multiple coins with same denom or coins are not sorted alphabetically

**Returns**:

bool validity

<a id="cosmpy.aerial.coins.sort_coins"></a>

#### sort`_`coins

```python
def sort_coins(coins: Union[Coins, List[Coin], List[CoinProto]])
```

Sort and validate coins collection based on Cosmos-SDK definition of Coins validity.

Coins collection must be sorted descending alphabetically based on denomination, and each denomination
in the collection must be unique = be present in the collection just once.

**Arguments**:

- `coins`: Coins to sort

