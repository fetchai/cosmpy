<a id="cosmpy.aerial.contract.__init__"></a>

# cosmpy.aerial.contract.`__`init`__`

cosmwasm contract functionality.

<a id="cosmpy.aerial.contract.__init__.LedgerContract"></a>

## LedgerContract Objects

```python
class LedgerContract(UserString)
```

Ledger contract.

<a id="cosmpy.aerial.contract.__init__.LedgerContract.__init__"></a>

#### `__`init`__`

```python
def __init__(path: Optional[str],
             client: LedgerClient,
             address: Optional[Address] = None,
             digest: Optional[bytes] = None,
             schema_path: Optional[str] = None,
             code_id: Optional[int] = None)
```

Initialize the Ledger contract.

**Arguments**:

- `path`: Path
- `client`: Ledger client
- `address`: address, defaults to None
- `digest`: digest, defaults to None
- `schema_path`: path to contract schema, defaults to None
- `code_id`: optional int. code id of the contract stored

<a id="cosmpy.aerial.contract.__init__.LedgerContract.path"></a>

#### path

```python
@property
def path() -> Optional[str]
```

Get contract path.

**Returns**:

contract path

<a id="cosmpy.aerial.contract.__init__.LedgerContract.digest"></a>

#### digest

```python
@property
def digest() -> Optional[bytes]
```

Get the contract digest.

**Returns**:

contract digest

<a id="cosmpy.aerial.contract.__init__.LedgerContract.code_id"></a>

#### code`_`id

```python
@property
def code_id() -> Optional[int]
```

Get the code id.

**Returns**:

code id

<a id="cosmpy.aerial.contract.__init__.LedgerContract.address"></a>

#### address

```python
@property
def address() -> Optional[Address]
```

Get the contract address.

**Returns**:

contract address

<a id="cosmpy.aerial.contract.__init__.LedgerContract.store"></a>

#### store

```python
def store(sender: Wallet,
          gas_limit: Optional[int] = None,
          memo: Optional[str] = None) -> int
```

Store the contract.

**Arguments**:

- `sender`: sender wallet address
- `gas_limit`: transaction gas limit, defaults to None
- `memo`: transaction memo, defaults to None

**Raises**:

- `RuntimeError`: Runtime error

**Returns**:

code id

<a id="cosmpy.aerial.contract.__init__.LedgerContract.instantiate"></a>

#### instantiate

```python
def instantiate(args: Any,
                sender: Wallet,
                label: Optional[str] = None,
                gas_limit: Optional[int] = None,
                admin_address: Optional[Address] = None,
                funds: Optional[str] = None) -> Address
```

Instantiate the contract.

**Arguments**:

- `args`: args
- `sender`: sender wallet address
- `label`: label, defaults to None
- `gas_limit`: transaction gas limit, defaults to None
- `admin_address`: admin address, defaults to None
- `funds`: funds, defaults to None

**Raises**:

- `RuntimeError`: Unable to extract contract code id

**Returns**:

contract address

<a id="cosmpy.aerial.contract.__init__.LedgerContract.deploy"></a>

#### deploy

```python
def deploy(args: Any,
           sender: Wallet,
           label: Optional[str] = None,
           store_gas_limit: Optional[int] = None,
           instantiate_gas_limit: Optional[int] = None,
           admin_address: Optional[Address] = None,
           funds: Optional[str] = None) -> Address
```

Deploy the contract.

**Arguments**:

- `args`: args
- `sender`: sender address
- `label`: label, defaults to None
- `store_gas_limit`: store gas limit, defaults to None
- `instantiate_gas_limit`: instantiate gas limit, defaults to None
- `admin_address`: admin address, defaults to None
- `funds`: funds, defaults to None

**Returns**:

instantiate contract details

<a id="cosmpy.aerial.contract.__init__.LedgerContract.execute"></a>

#### execute

```python
def execute(args: Any,
            sender: Wallet,
            gas_limit: Optional[int] = None,
            funds: Optional[str] = None) -> SubmittedTx
```

execute the contract.

**Arguments**:

- `args`: args
- `sender`: sender address
- `gas_limit`: transaction gas limit, defaults to None
- `funds`: funds, defaults to None

**Raises**:

- `RuntimeError`: Contract appears not to be deployed currently

**Returns**:

transaction details broadcast

<a id="cosmpy.aerial.contract.__init__.LedgerContract.query"></a>

#### query

```python
def query(args: Any) -> Any
```

Query on contract.

**Arguments**:

- `args`: args

**Raises**:

- `RuntimeError`: Contract appears not to be deployed currently

**Returns**:

query result

<a id="cosmpy.aerial.contract.__init__.LedgerContract.data"></a>

#### data

```python
@property
def data()
```

Get the contract address.

**Returns**:

contract address

<a id="cosmpy.aerial.contract.__init__.LedgerContract.__json__"></a>

#### `__`json`__`

```python
def __json__()
```

Get the contract details in json.

**Returns**:

contract details in json

