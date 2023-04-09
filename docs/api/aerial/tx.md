<a id="c4epy.aerial.tx"></a>

# c4epy.aerial.tx

Transaction.

<a id="c4epy.aerial.tx.TxState"></a>

## TxState Objects

```python
class TxState(Enum)
```

Transaction state.

**Arguments**:

- `Enum`: Draft, Sealed, Final

<a id="c4epy.aerial.tx.SigningMode"></a>

## SigningMode Objects

```python
class SigningMode(Enum)
```

Signing mode.

**Arguments**:

- `Enum`: Direct

<a id="c4epy.aerial.tx.SigningCfg"></a>

## SigningCfg Objects

```python
@dataclass
class SigningCfg()
```

Transaction signing configuration.

<a id="c4epy.aerial.tx.SigningCfg.direct"></a>

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

<a id="c4epy.aerial.tx.Transaction"></a>

## Transaction Objects

```python
class Transaction()
```

Transaction.

<a id="c4epy.aerial.tx.Transaction.__init__"></a>

#### `__`init`__`

```python
def __init__()
```

Init the Transactions with transaction message, state, fee and body.

<a id="c4epy.aerial.tx.Transaction.state"></a>

#### state

```python
@property
def state() -> TxState
```

Get the transaction state.

**Returns**:

current state of the transaction

<a id="c4epy.aerial.tx.Transaction.msgs"></a>

#### msgs

```python
@property
def msgs()
```

Get the transaction messages.

**Returns**:

transaction messages

<a id="c4epy.aerial.tx.Transaction.fee"></a>

#### fee

```python
@property
def fee() -> Optional[str]
```

Get the transaction fee.

**Returns**:

transaction fee

<a id="c4epy.aerial.tx.Transaction.tx"></a>

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

<a id="c4epy.aerial.tx.Transaction.add_message"></a>

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

<a id="c4epy.aerial.tx.Transaction.seal"></a>

#### seal

```python
def seal(signing_cfgs: Union[SigningCfg, List[SigningCfg]],
         fee: str,
         gas_limit: int,
         memo: Optional[str] = None) -> "Transaction"
```

Seal the transaction.

**Arguments**:

- `signing_cfgs`: signing configs
- `fee`: transaction fee
- `gas_limit`: transaction gas limit
- `memo`: transaction memo, defaults to None

**Returns**:

sealed transaction.

<a id="c4epy.aerial.tx.Transaction.sign"></a>

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

<a id="c4epy.aerial.tx.Transaction.complete"></a>

#### complete

```python
def complete() -> "Transaction"
```

Update transaction state to Final.

**Returns**:

transaction with  updated state

