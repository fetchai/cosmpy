<a id="cosmpy.aerial.client.base"></a>

# cosmpy.aerial.client.base

Functionality shared between the sync and async ledger clients.

Everything in this module is I/O free: configuration handling, request/response
translation and fee arithmetic. The network calls themselves live in the
concrete clients (``LedgerClient`` and ``AsyncLedgerClient``), which both
operate on the same generated protobuf stubs.

<a id="cosmpy.aerial.client.base.LedgerClientBase"></a>

## LedgerClientBase Objects

```python
class LedgerClientBase()
```

Ledger client base with the functionality shared by the sync and async clients.

<a id="cosmpy.aerial.client.base.LedgerClientBase.__init__"></a>

#### `__`init`__`

```python
def __init__(cfg: NetworkConfig,
             query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
             query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS)
```

Init ledger client base.

**Arguments**:

- `cfg`: Network configurations
- `query_interval_secs`: int. optional interval int seconds
- `query_timeout_secs`: int. optional interval int seconds

<a id="cosmpy.aerial.client.base.LedgerClientBase.network_config"></a>

#### network`_`config

```python
@property
def network_config() -> NetworkConfig
```

Get the network config.

**Returns**:

network config

<a id="cosmpy.aerial.client.base.LedgerClientBase.estimate_fee_from_gas"></a>

#### estimate`_`fee`_`from`_`gas

```python
def estimate_fee_from_gas(gas_limit: int) -> str
```

Estimate fee from gas.

**Arguments**:

- `gas_limit`: gas limit

**Returns**:

Estimated fee for transaction

