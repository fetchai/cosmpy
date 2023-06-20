<a id="cosmpy.aerial.faucet"></a>

# cosmpy.aerial.faucet

Ledger faucet API interface.

<a id="cosmpy.aerial.faucet.FaucetApi"></a>

## FaucetApi Objects

```python
class FaucetApi()
```

Faucet API.

<a id="cosmpy.aerial.faucet.FaucetApi.FAUCET_STATUS_PENDING"></a>

#### FAUCET`_`STATUS`_`PENDING

noqa: F841

<a id="cosmpy.aerial.faucet.FaucetApi.FAUCET_STATUS_PROCESSING"></a>

#### FAUCET`_`STATUS`_`PROCESSING

noqa: F841

<a id="cosmpy.aerial.faucet.FaucetApi.FAUCET_STATUS_COMPLETED"></a>

#### FAUCET`_`STATUS`_`COMPLETED

noqa: F841

<a id="cosmpy.aerial.faucet.FaucetApi.FAUCET_STATUS_FAILED"></a>

#### FAUCET`_`STATUS`_`FAILED

noqa: F841

<a id="cosmpy.aerial.faucet.FaucetApi.__init__"></a>

#### `__`init`__`

```python
def __init__(net_config: NetworkConfig)
```

Init faucet API.

**Arguments**:

- `net_config`: Ledger network configuration.

**Raises**:

- `ValueError`: Network config has no faucet url set

<a id="cosmpy.aerial.faucet.FaucetApi.get_wealth"></a>

#### get`_`wealth

```python
def get_wealth(address: Union[Address, str]) -> None
```

Get wealth from the faucet for the provided address.

**Arguments**:

- `address`: the address.

**Raises**:

- `RuntimeError`: Unable to create faucet claim
- `RuntimeError`: Failed to check faucet claim status
- `RuntimeError`: Failed to get wealth for address
- `ValueError`: Faucet claim check timed out

