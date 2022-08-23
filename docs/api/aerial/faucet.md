<a id="cosmpy.aerial.faucet"></a>

# cosmpy.aerial.faucet

Ledger faucet API interface.

<a id="cosmpy.aerial.faucet.FaucetApi"></a>

## FaucetApi Objects

```python
class FaucetApi()
```

Faucet API.

<a id="cosmpy.aerial.faucet.FaucetApi.__init__"></a>

#### `__`init`__`

```python
def __init__(net_config: NetworkConfig)
```

Init faucet API.

**Arguments**:

- `net_config`: Ledger network configuration.

<a id="cosmpy.aerial.faucet.FaucetApi.get_wealth"></a>

#### get`_`wealth

```python
def get_wealth(address: Union[Address, str]) -> None
```

Get wealth from the faucet for the provided address.

**Arguments**:

- `address`: the address.

**Raises**:

- `None`: RuntimeError of explicit faucet failures

