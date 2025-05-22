<a id="cosmpy.aerial.tx"></a>

# cosmpy.aerial.tx

Transaction.

<a id="cosmpy.aerial.tx.TxFee"></a>

## TxFee Objects

```python
@dataclass
class TxFee()
```

Cosmos SDK TxFee abstraction.

Example::
from cosmpy.aerial.tx import TxFee
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto

fee = TxFee()
fee = TxFee(amount="1000afet")
fee = TxFee(amount=CoinProto(amount=str(1000), denom="afet"))
fee = TxFee(amount="100afet,10uatom")
fee = TxFee(amount=[CoinProto(amount=str(100), denom="afet"),CoinProto(amount=str(10), denom="uatom")])

<a id="cosmpy.aerial.tx.TxFee.__init__"></a>

#### `__`init`__`

```python
def __init__(amount: Optional[CoinsParamType] = None,
             gas_limit: Optional[int] = None,
             granter: Optional[Address] = None,
             payer: Optional[Address] = None)
```

Initialize a TxFee object.

**Arguments**:

- `amount`: The transaction fee amount, as a Coin, list of Coins, or string (e.g., "100uatom").
- `gas_limit`: Optional gas limit for the transaction.
- `granter`: Optional address of the fee granter.
- `payer`: Optional address of the fee payer.

<a id="cosmpy.aerial.tx.TxFee.amount"></a>

#### amount

```python
@property
def amount() -> Optional[List[Coin]]
```

Set the transaction fee amount.

Accepts a string, Coin, or list of Coins and converts to a canonical list of Coin objects.

**Returns**:

amount as Optional[List[Coin]]

<a id="cosmpy.aerial.tx.TxFee.amount"></a>

#### amount

```python
@amount.setter
def amount(value: Optional[CoinsParamType])
```

Set amount.

Ensures conversion to Optional[List[Coin]]

**Arguments**:

- `value`: The amount value to set using str or Coin or List[Coin] representation of the amount value

<a id="cosmpy.aerial.tx.TxFee.to_proto"></a>

#### to`_`proto

```python
def to_proto() -> Fee
```

Return protobuf representation of TxFee.

**Raises**:

- `RuntimeError`: Gas limit must be set

**Returns**:

Fee

<a id="cosmpy.aerial.tx.TxState"></a>

## TxState Objects

```python
class TxState(Enum)
```

Transaction state.

**Arguments**:

- `Enum`: Draft, Sealed, Final

<a id="cosmpy.aerial.tx.SigningMode"></a>

## SigningMode Objects

```python
class SigningMode(Enum)
```

Signing mode.

**Arguments**:

- `Enum`: Direct

<a id="cosmpy.aerial.tx.SigningCfg"></a>

## SigningCfg Objects

```python
@dataclass
class SigningCfg()
```

Transaction signing configuration.

<a id="cosmpy.aerial.tx.SigningCfg.direct"></a>

#### direct

```python
@staticmethod
def direct(public_key: PublicKey, sequence_num: int) -> "SigningCfg"
```

Transaction signing configuration using direct mode.

**Arguments**:

- `public_key`: public key
- `sequence_num`: sequence number

**Returns**:

Transaction signing configuration

<a id="cosmpy.aerial.tx.Transaction"></a>

## Transaction Objects

```python
class Transaction()
```

Transaction.

<a id="cosmpy.aerial.tx.Transaction.__init__"></a>

#### `__`init`__`

```python
def __init__()
```

Init the Transactions with transaction message, state, fee and body.

<a id="cosmpy.aerial.tx.Transaction.state"></a>

#### state

```python
@property
def state() -> TxState
```

Get the transaction state.

**Returns**:

current state of the transaction

<a id="cosmpy.aerial.tx.Transaction.msgs"></a>

#### msgs

```python
@property
def msgs()
```

Get the transaction messages.

**Returns**:

transaction messages

<a id="cosmpy.aerial.tx.Transaction.fee"></a>

#### fee

```python
@property
def fee() -> Optional[Fee]
```

Get the transaction fee.

**Returns**:

transaction fee

<a id="cosmpy.aerial.tx.Transaction.tx"></a>

#### tx

```python
@property
def tx()
```

Initialize.

**Raises**:

- `RuntimeError`: If the transaction has not been completed.

**Returns**:

transaction

<a id="cosmpy.aerial.tx.Transaction.add_message"></a>

#### add`_`message

```python
def add_message(msg: Any) -> "Transaction"
```

Initialize.

**Arguments**:

- `msg`: transaction message (memo)

**Raises**:

- `RuntimeError`: If the transaction is not in the draft state.

**Returns**:

transaction with message added

<a id="cosmpy.aerial.tx.Transaction.seal"></a>

#### seal

```python
def seal(signing_cfgs: Union[SigningCfg, List[SigningCfg]],
         fee: TxFee,
         memo: Optional[str] = None,
         timeout_height: Optional[int] = None) -> "Transaction"
```

Seal the transaction.

**Arguments**:

- `signing_cfgs`: signing configs
- `fee`: transaction fee class
- `memo`: transaction memo, defaults to None
- `timeout_height`: timeout height, defaults to None

**Returns**:

sealed transaction.

<a id="cosmpy.aerial.tx.Transaction.sign"></a>

#### sign

```python
def sign(signer: Signer,
         chain_id: str,
         account_number: int,
         deterministic: bool = False) -> "Transaction"
```

Sign the transaction.

**Arguments**:

- `signer`: Signer
- `chain_id`: chain id
- `account_number`: account number
- `deterministic`: deterministic, defaults to False

**Raises**:

- `RuntimeError`: If transaction is not sealed

**Returns**:

signed transaction

<a id="cosmpy.aerial.tx.Transaction.complete"></a>

#### complete

```python
def complete() -> "Transaction"
```

Update transaction state to Final.

**Returns**:

transaction with  updated state

