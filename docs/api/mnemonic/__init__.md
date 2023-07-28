<a id="cosmpy.mnemonic.__init__"></a>

# cosmpy.mnemonic.`__`init`__`

Mnemonic implementation.

<a id="cosmpy.mnemonic.__init__.split_hmac"></a>

#### split`_`hmac

```python
def split_hmac(data: bytes) -> Tuple[bytes, bytes]
```

Split HMAC data into two halves.

**Arguments**:

- `data`: bytes

**Returns**:

Tuple[bytes, bytes]

<a id="cosmpy.mnemonic.__init__.validate_private_key"></a>

#### validate`_`private`_`key

```python
def validate_private_key(private_key: bytes) -> bool
```

Validate the private key.

**Arguments**:

- `private_key`: bytes

**Returns**:

bool

<a id="cosmpy.mnemonic.__init__.derive_master_key"></a>

#### derive`_`master`_`key

```python
def derive_master_key(seed_bytes: bytes) -> Tuple[bytes, bytes]
```

Derive the master key and chain code from the seed bytes.

**Arguments**:

- `seed_bytes`: bytes

**Raises**:

- `ValueError`: If the seed length is invalid.

**Returns**:

Tuple[bytes, bytes]

<a id="cosmpy.mnemonic.__init__.parse_derivation_path"></a>

#### parse`_`derivation`_`path

```python
def parse_derivation_path(path: str) -> List[int]
```

Parse the derivation path in the form of m/44'/118'/0'/0/0 and return a list of indexes.

**Arguments**:

- `path`: str

**Raises**:

- `RuntimeError`: If the derivation path is invalid.

**Returns**:

List[int]

<a id="cosmpy.mnemonic.__init__.derive_child_key_from_index"></a>

#### derive`_`child`_`key`_`from`_`index

```python
def derive_child_key_from_index(private_key: bytes, chain_code: bytes,
                                index: int) -> Tuple[bytes, bytes]
```

Derive a child key from the specified private key, chain code, and index.

**Arguments**:

- `private_key`: bytes
- `chain_code`: bytes
- `index`: int

**Returns**:

Tuple[bytes, bytes]

<a id="cosmpy.mnemonic.__init__.derive_child_key"></a>

#### derive`_`child`_`key

```python
def derive_child_key(master_private_key: bytes, chain_code: bytes,
                     path: str) -> bytes
```

Derive a child key from a master key and a derivation path.

**Arguments**:

- `master_private_key`: bytes The master private key.
- `chain_code`: bytes The chain code.
- `path`: str The derivation path.

**Returns**:

bytes The derived child key.

<a id="cosmpy.mnemonic.__init__.validate_mnemonic_and_normalise"></a>

#### validate`_`mnemonic`_`and`_`normalise

```python
def validate_mnemonic_and_normalise(mnemonic: str) -> str
```

Validate a mnemonic phrase.

**Arguments**:

- `mnemonic`: str The mnemonic phrase to validate.

**Raises**:

- `ValueError`: If the mnemonic length is invalid or a word is invalid.

**Returns**:

str The normalized mnemonic phrase.

<a id="cosmpy.mnemonic.__init__.derive_seed_from_mnemonic"></a>

#### derive`_`seed`_`from`_`mnemonic

```python
def derive_seed_from_mnemonic(mnemonic: str,
                              passphrase: Optional[str] = None) -> bytes
```

Derive a seed from a mnemonic phrase.

**Arguments**:

- `mnemonic`: str The mnemonic phrase.
- `passphrase`: Optional[str] An optional passphrase.

**Returns**:

bytes The derived seed as bytes.

<a id="cosmpy.mnemonic.__init__.derive_child_key_from_mnemonic"></a>

#### derive`_`child`_`key`_`from`_`mnemonic

```python
def derive_child_key_from_mnemonic(mnemonic: str,
                                   passphrase: Optional[str] = None,
                                   path: str = COSMOS_HD_PATH) -> bytes
```

Derive a child key from a mnemonic phrase and a derivation path.

**Arguments**:

- `mnemonic`: str The mnemonic phrase.
- `passphrase`: Optional[str] An optional passphrase.
- `path`: str The derivation path.

**Returns**:

bytes The derived child key.

<a id="cosmpy.mnemonic.__init__.entropy_to_mnemonic"></a>

#### entropy`_`to`_`mnemonic

```python
def entropy_to_mnemonic(entropy: bytes) -> str
```

Convert entropy bytes to a mnemonic phrase.

**Arguments**:

- `entropy`: bytes The entropy bytes.

**Raises**:

- `ValueError`: If the data length is invalid.

**Returns**:

str The generated mnemonic phrase.

<a id="cosmpy.mnemonic.__init__.generate_entropy"></a>

#### generate`_`entropy

```python
def generate_entropy(num_bits: int) -> bytes
```

Generate entropy bytes.

**Arguments**:

- `num_bits`: int The number of bits for the entropy.

**Returns**:

bytes The generated entropy bytes.

<a id="cosmpy.mnemonic.__init__.generate_mnemonic"></a>

#### generate`_`mnemonic

```python
def generate_mnemonic(num_bits=256)
```

Generate a mnemonic phrase.

**Arguments**:

- `num_bits`: int The number of bits for the entropy.

**Returns**:

str The generated mnemonic phrase.

