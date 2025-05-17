<a id="cosmpy.aerial.client.types"></a>

# cosmpy.aerial.client.types

Types.

<a id="cosmpy.aerial.client.types.Coin"></a>

## Coin Objects

```python
@dataclass
class Coin()
```

Coins.

<a id="cosmpy.aerial.client.types.Coin.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> CoinProto
```

Convert this type to protobuf schema Coin type.

<a id="cosmpy.aerial.client.types.Account"></a>

## Account Objects

```python
@dataclass
class Account()
```

Account.

<a id="cosmpy.aerial.client.types.Block"></a>

## Block Objects

```python
@dataclass
class Block()
```

Block.

<a id="cosmpy.aerial.client.types.Block.from_proto"></a>

#### from`_`proto

```python
@staticmethod
def from_proto(block: Any) -> "Block"
```

Parse the block.

**Arguments**:

- `block`: block as Any

**Returns**:

parsed block as Block

