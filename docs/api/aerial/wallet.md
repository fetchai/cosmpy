<a id="cosmpy.aerial.wallet"></a>

# cosmpy.aerial.wallet

Wallet Generation.

<a id="cosmpy.aerial.wallet.Wallet"></a>

## Wallet Objects

```python
class Wallet(ABC, UserString)
```

Wallet Generation

**Arguments**:

- `ABC`: ABC abstract method
- `UserString`: user string

<a id="cosmpy.aerial.wallet.Wallet.address"></a>

#### address

```python
@abstractmethod
def address() -> Address
```

get the address of the wallet

**Returns**:

None

<a id="cosmpy.aerial.wallet.Wallet.public_key"></a>

#### public`_`key

```python
@abstractmethod
def public_key() -> PublicKey
```

get the public key of the wallet

**Returns**:

None

<a id="cosmpy.aerial.wallet.Wallet.signer"></a>

#### signer

```python
@abstractmethod
def signer() -> Signer
```

get the signer of the wallet

**Returns**:

None

<a id="cosmpy.aerial.wallet.Wallet.data"></a>

#### data

```python
@property
def data()
```

Get the address of the wallet

**Returns**:

Address

<a id="cosmpy.aerial.wallet.Wallet.__json__"></a>

#### `__`json`__`

```python
def __json__()
```

stringify the address

**Returns**:

address in string format

<a id="cosmpy.aerial.wallet.LocalWallet"></a>

## LocalWallet Objects

```python
class LocalWallet(Wallet)
```

Generate local wallet

**Arguments**:

- `Wallet`: wallet

<a id="cosmpy.aerial.wallet.LocalWallet.generate"></a>

#### generate

```python
@staticmethod
def generate(prefix: Optional[str] = None) -> "LocalWallet"
```

generate the local wallet

**Arguments**:

- `prefix`: prefix, defaults to None

**Returns**:

local wallet

<a id="cosmpy.aerial.wallet.LocalWallet.from_mnemonic"></a>

#### from`_`mnemonic

```python
@staticmethod
def from_mnemonic(mnemonic: str,
                  prefix: Optional[str] = None) -> "LocalWallet"
```

Generate local wallet from mnemonic

**Arguments**:

- `mnemonic`: mnemonic
- `prefix`: prefix, defaults to None

**Returns**:

local wallet

<a id="cosmpy.aerial.wallet.LocalWallet.from_unsafe_seed"></a>

#### from`_`unsafe`_`seed

```python
@staticmethod
def from_unsafe_seed(text: str,
                     index: Optional[int] = None,
                     prefix: Optional[str] = None) -> "LocalWallet"
```

Generate local wallet from unsafe seed.

**Arguments**:

- `text`: text
- `index`: index, defaults to None
- `prefix`: prefix, defaults to None

**Returns**:

Local wallet

<a id="cosmpy.aerial.wallet.LocalWallet.__init__"></a>

#### `__`init`__`

```python
def __init__(private_key: PrivateKey, prefix: Optional[str] = None)
```

Init wallet with

**Arguments**:

- `private_key`: private key of the wallet
- `prefix`: prefix, defaults to None

<a id="cosmpy.aerial.wallet.LocalWallet.address"></a>

#### address

```python
def address() -> Address
```

Get the wallet address.

**Returns**:

Wallet address.

<a id="cosmpy.aerial.wallet.LocalWallet.public_key"></a>

#### public`_`key

```python
def public_key() -> PublicKey
```

Get the public key of the wallet

**Returns**:

public key

<a id="cosmpy.aerial.wallet.LocalWallet.signer"></a>

#### signer

```python
def signer() -> PrivateKey
```

Get  the signer of the wallet.

**Returns**:

signer

