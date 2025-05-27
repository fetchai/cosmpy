<a id="cosmpy.aerial.types"></a>

# cosmpy.aerial.types

Types.

<a id="cosmpy.aerial.types.Account"></a>

## Account Objects

```python
@dataclass
class Account()
```

Account.

<a id="cosmpy.aerial.types.Block"></a>

## Block Objects

```python
@dataclass
class Block()
```

Block.

<a id="cosmpy.aerial.types.Block.from_proto"></a>

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

