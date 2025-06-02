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

<a id="cosmpy.aerial.coins.Coin.__init__"></a>

#### `__`init`__`

```python
def __init__(amount: int, denom: str) -> None
```

Create Coin instance.

<a id="cosmpy.aerial.coins.Coin.__repr__"></a>

#### `__`repr`__`

```python
def __repr__() -> str
```

Return string representation of coin.

<a id="cosmpy.aerial.coins.Coin.denom"></a>

#### denom

```python
@property
def denom() -> str
```

Return denom of coin.

The denom property setter is *NOT* defined *by-design* in order to avoid misalignment/inconsistencies
later on in the `Coins` collection class.
If the denom setter was enabled, then it would allow changing denom value externally = from without knowledge
of the `Coins` collection class, since the `Coin` is reference type. We want to avoid passing the Coin instance
always by-value (by-copy).

**Returns**:

denomination of the coin instance

<a id="cosmpy.aerial.coins.Coin.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> CoinProto
```

Convert this type to protobuf schema Coin type.

<a id="cosmpy.aerial.coins.Coin.is_valid"></a>

#### is`_`valid

```python
def is_valid(raise_ex: bool = False) -> bool
```

Validate Coin instance based on Cosmos-SDK requirements.

**Arguments**:

- `raise_ex`: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

**Returns**:

True if the Coin instance conforms to cosmos-sdk requirement for Coin, False otherwise.

<a id="cosmpy.aerial.coins.Coin.is_amount_valid"></a>

#### is`_`amount`_`valid

```python
def is_amount_valid(raise_ex: bool = False) -> bool
```

Validate amount value based on Cosmos-SDK requirements.

**Arguments**:

- `raise_ex`: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

**Raises**:

- `ValueError`: If `raise_ex` is True and amount does not conform to cosmos-sdk requirement.

**Returns**:

True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than
or equal to  zero). False otherwise.

<a id="cosmpy.aerial.coins.Coin.is_denom_valid"></a>

#### is`_`denom`_`valid

```python
def is_denom_valid(raise_ex: bool = False) -> bool
```

Validate denom value based on Cosmos-SDK requirements.

**Arguments**:

- `raise_ex`: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

**Returns**:

True if denom conforms to cosmos-sdk requirement for denomination, False otherwise.

<a id="cosmpy.aerial.coins.OnCollision"></a>

## OnCollision Objects

```python
class OnCollision(Enum)
```

OnCollision Enum.

<a id="cosmpy.aerial.coins.Coins"></a>

## Coins Objects

```python
class Coins()
```

Coins.

<a id="cosmpy.aerial.coins.Coins.__init__"></a>

#### `__`init`__`

```python
def __init__(coins: Optional[Union[str, "Coins", List[Coin], List[CoinProto],
                                   Coin, CoinProto]] = None)
```

Instantiate Coins from any of the supported coin(s) representation types.

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

<a id="cosmpy.aerial.coins.Coins.__iter__"></a>

#### `__`iter`__`

```python
def __iter__()
```

Get coins iterator.

<a id="cosmpy.aerial.coins.Coins.__len__"></a>

#### `__`len`__`

```python
def __len__() -> int
```

Get number of coins.

<a id="cosmpy.aerial.coins.Coins.__getitem__"></a>

#### `__`getitem`__`

```python
def __getitem__(denom: str) -> Coin
```

Coins safe getter that prevents modifying of the reference.

<a id="cosmpy.aerial.coins.Coins.__contains__"></a>

#### `__`contains`__`

```python
def __contains__(denom: str) -> bool
```

Return true if denom is present.

<a id="cosmpy.aerial.coins.Coins.__delitem__"></a>

#### `__`delitem`__`

```python
def __delitem__(denom: str)
```

Remove denom.

<a id="cosmpy.aerial.coins.Coins.__eq__"></a>

#### `__`eq`__`

```python
def __eq__(right) -> bool
```

Compare if two instances of Coins are equal.

<a id="cosmpy.aerial.coins.Coins.__hash__"></a>

#### `__`hash`__`

```python
def __hash__() -> int
```

Hash.

<a id="cosmpy.aerial.coins.Coins.clear"></a>

#### clear

```python
def clear()
```

Delete all coins.

<a id="cosmpy.aerial.coins.Coins.assign"></a>

#### assign

```python
def assign(coins: Optional[Union[str, "Coins", List[Coin], List[CoinProto],
                                 Coin, CoinProto]] = None)
```

Assign value of this ('self') instance from any of the supported coin(s) representation types.

**Arguments**:

- `coins`: Input coins in any of supported types.

**Raises**:

- `TypeError`: If coins or coin in a list has unexpected type
This means that the current value of this ('self') instance will be completely replaced with a new value
carried in the input `coins` parameter.

<a id="cosmpy.aerial.coins.Coins.merge_from"></a>

#### merge`_`from

```python
def merge_from(coins: Union[str, "Coins", List[Coin], List[CoinProto], Coin,
                            CoinProto],
               on_collision: OnCollision = OnCollision.Fail) -> "Coins"
```

Merge passed in coins in to this ('self') coins instance.

**Arguments**:

- `coins`: Input coins in any of supported types.
- `on_collision`: If OnCollision.Override then the coin instance in this (self) object will be overridden if it already
contains the denomination, if OnCollision.Fail the merge will fail with exception.

**Returns**:

The `self` instance containing merged coins

<a id="cosmpy.aerial.coins.Coins.get"></a>

#### get

```python
def get(denom: str, default_amount: int) -> Coin
```

Return Coin instance for the given `denom`.

If coin with the given `denom` is not present, the `default` will be returned.

Runtime complexity: `O(log(n))`

This method poses the same risk to validity of the Coins value as the `__getitem__(...)` method,
since at the moment it returns Coin instance *by-reference* what allows to change the `Coin.amount` value
from external context and so potentially invalidate the value represented by the `Coins` class/container.

**Arguments**:

- `denom`: denomination of the coin to query.
- `default_amount`: default amount used to construct returned Coin instance if there is *no* coin with
the given `denom` present in this coins instance.

**Returns**:

coin instance for the given `denom`, or the `default` value.
Example::
>>> from cosmpy.aerial.coins import Coin, Coins
>>> cs = Coins("1aaa,2baa,3caa")
>>> cs.get("baa", 0)
2baa
>>> cs.get("ggg", 0)
0ggg

<a id="cosmpy.aerial.coins.Coins.get_by_index"></a>

#### get`_`by`_`index

```python
def get_by_index(index: int) -> Coin
```

Return Coin instance at given `index`.

If the `index` is out of range, raises :exc:`IndexError`.

Runtime complexity: `O(log(n))`

This method poses the same risk to validity of the Coins value as the `__getitem__(...)` method,
since at the moment it returns Coin instance *by-reference* what allows to change the `Coin.amount` value
from external context and so potentially invalidate the value represented by the `Coins` class/container.

Example::
>>> from cosmpy.aerial.coins import Coin, Coins
>>> cs = Coins("1aaa,2baa,3caa")
>>> cs.get_by_index(0)
1aaa
>>> cs.get_by_index(2)
3caa
>>> cs.get_by_index(3)
Traceback (most recent call last):
  ...
IndexError: list index out of range

**Arguments**:

- `index`: int index of item (default -1)

**Returns**:

key and value pair

<a id="cosmpy.aerial.coins.Coins.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> List[CoinProto]
```

Convert this type to *protobuf schema* Coins type.

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

<a id="cosmpy.aerial.coins.from_string"></a>

#### from`_`string

```python
def from_string(value: str)
```

Parse the coins string and yields individual coins as Coin instances in order of their definition in input `value`.

**Arguments**:

- `value`: coins

**Raises**:

- `RuntimeError`: If unable to parse the value

**Returns**:

Coin objects one by one in the order they are specified in the input `value` string, where validation of
the yielded Coin instance is intentionally *NOT* executed => yielded coin instance might *NOT* be valid
when judged based on cosmos-sdk requirements.
This is by-design to enable just basic parsing focused exclusively on the format of the coins string value.
This leaves a degree of freedom for a caller on how the resulting/parsed coins should be used/consumed,
rather than forcing any checks/validation for individual coins instances, or coins collection as a whole,
here.

<a id="cosmpy.aerial.coins.is_denom_valid"></a>

#### is`_`denom`_`valid

```python
def is_denom_valid(denom: str, raise_ex: bool = False) -> bool
```

Check if denom value conforms to Cosmos-SDK requirements.

**Arguments**:

- `denom`: Denom to be checked
- `raise_ex`: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

**Raises**:

- `ValueError`: If `raise_ex` is True and amount does not conform to cosmos-sdk requirement.

**Returns**:

True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than zero),
False otherwise.

<a id="cosmpy.aerial.coins.is_coins_sorted"></a>

#### is`_`coins`_`sorted

```python
def is_coins_sorted(
        coins: Union[str, Coins, Iterable[Coin], Iterable[CoinProto]]) -> bool
```

Return true if given coins representation is sorted in ascending order of denom.

**Arguments**:

- `coins`: Any type representing coins

**Returns**:

bool is_sorted

<a id="cosmpy.aerial.coins.validate_coins"></a>

#### validate`_`coins

```python
def validate_coins(coins: Union[str, Coins, Iterable[Coin],
                                Iterable[CoinProto]])
```

Return true if given coins representation is valid.

raises ValueError if there are multiple coins with the same denom

**Arguments**:

- `coins`: Any type representing coins

**Returns**:

bool validity

