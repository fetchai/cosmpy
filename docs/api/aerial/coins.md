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

**Raises**:

- `ValueError`: If amount is negative or denom does not conform to cosmos-sdk requirement for denomination.

<a id="cosmpy.aerial.coins.Coin.is_valid"></a>

#### is`_`valid

```python
def is_valid() -> bool
```

Validate Coin instance based on Cosmos-SDK requirements.

**Returns**:

True if the Coin instance conforms to cosmos-sdk requirement for Coin, False otherwise.

<a id="cosmpy.aerial.coins.Coin.is_amount_valid"></a>

#### is`_`amount`_`valid

```python
def is_amount_valid() -> bool
```

Validate amount value based on Cosmos-SDK requirements.

**Returns**:

True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than zero),
False otherwise.

<a id="cosmpy.aerial.coins.Coin.is_denom_valid"></a>

#### is`_`denom`_`valid

```python
def is_denom_valid() -> bool
```

Validate denom value based on Cosmos-SDK requirements.

**Returns**:

True if denom conforms to cosmos-sdk requirement for denomination, False otherwise.

<a id="cosmpy.aerial.coins.Coins"></a>

## Coins Objects

```python
class Coins(List[Coin])
```

Coins.

It is required to call the 'canonicalise()' method in order to ensure that the Coins instance conforms to
Cosmos-SDK requirements for Coins type!
This is because one way or another, due to the nature of the base List type, it is possible to create such an
instance of Coins which does not conform to Cosmos-SDK requirements.

<a id="cosmpy.aerial.coins.Coins.__init__"></a>

#### `__`init`__`

```python
def __init__(coins: Optional[Union[str, "Coins", List[Coin], List[CoinProto],
                                   Coin, CoinProto]] = None)
```

Convert any coin representation into Coins.

<a id="cosmpy.aerial.coins.Coins.__repr__"></a>

#### `__`repr`__`

```python
def __repr__() -> str
```

Return cosmos-sdk string representation of Coins.

**Returns**:

cosmos-sdk formatted string representation of Coins.
Example::
from cosmpy.aerial.client.coins import Coin, Coins

coins = Coins([Coin(1,"afet"), Coin(2,"uatom"), Coin(3,"nanomobx")])
assert str(coins) == "1afet,2uatom,3nanomobx"

<a id="cosmpy.aerial.coins.Coins.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> List[CoinProto]
```

Convert this type to *protobuf schema* Coins type.

<a id="cosmpy.aerial.coins.Coins.canonicalise"></a>

#### canonicalise

```python
def canonicalise() -> "Coins"
```

Reorganise the value of the 'self' instance in to canonical form defined by cosmos-sdk for `Coins`.

This means dropping all coins with zero value, and alphabetically sorting (ascending) the coins based
on denomination.
The algorithm *fails* with exception *if* any of the denominations in the list is *not* unique = if some of the
denominations are present in the coin list more than once, or if validation of any individual coin will fail.

**Returns**:

The 'self' instance.

<a id="cosmpy.aerial.coins.Coins.validate"></a>

#### validate

```python
def validate()
```

Validate whether current value conforms to canonical form for list of coins defined by cosmos-sdk.

Raises ValueError exception *IF* denominations are not unique, or if validation of individual coins raises an
exception.

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

Perform algebraic vector subtraction of two coin lists, ensuring no coin has negative value.

<a id="cosmpy.aerial.coins.Coins.__iadd__"></a>

#### `__`iadd`__`

```python
def __iadd__(other)
```

Perform *in-place* algebraic vector subtraction of two coin lists.

<a id="cosmpy.aerial.coins.Coins.__isub__"></a>

#### `__`isub`__`

```python
def __isub__(other)
```

Perform *in-place* algebraic vector subtraction of two coin lists, ensuring no coin has negative value.

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

Return true if given coins representation is sorted in ascending order of denom.

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

- `ValueError`: If there are multiple coins with the same denom

**Returns**:

bool validity

<a id="cosmpy.aerial.coins.sort_coins"></a>

#### sort`_`coins

```python
def sort_coins(coins: Union[Coins, List[Coin], List[CoinProto]])
```

Sort the collection of coins based on Cosmos-SDK definition of Coins validity.

Coins collection is sorted ascending alphabetically based on denomination.

NOTE: The resulting sorted collection of coins is *NOT* validated by calling the 'Coins.validate()'.

**Arguments**:

- `coins`: Coins to sort

