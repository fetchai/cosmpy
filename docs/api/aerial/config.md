<a id="cosmpy.aerial.config"></a>

# cosmpy.aerial.config

Network configurations.

<a id="cosmpy.aerial.config.NetworkConfigError"></a>

## NetworkConfigError Objects

```python
class NetworkConfigError(RuntimeError)
```

Network config error.

**Arguments**:

- `RuntimeError`: Runtime error

<a id="cosmpy.aerial.config.NetworkConfig"></a>

## NetworkConfig Objects

```python
@dataclass
class NetworkConfig()
```

Network configurations.

**Raises**:

- `NetworkConfigError`: Network config error
- `RuntimeError`: Runtime error

<a id="cosmpy.aerial.config.NetworkConfig.validate"></a>

#### validate

```python
def validate()
```

Validate the network configuration.

**Raises**:

- `NetworkConfigError`: Network config error

<a id="cosmpy.aerial.config.NetworkConfig.chain4energy_veles_testnet"></a>

#### chain4energy`_`veles`_`testnet

```python
@classmethod
def chain4energy_veles_testnet(cls) -> "NetworkConfig"
```

Chain4energy veles testnet.

**Returns**:

Network configuration

<a id="cosmpy.aerial.config.NetworkConfig.chain4energy_alpha_testnet"></a>

#### chain4energy`_`alpha`_`testnet

```python
@classmethod
def chain4energy_alpha_testnet(cls)
```

Get the Chain4energy alpha testnet.

**Raises**:

- `RuntimeError`: No alpha testnet available

<a id="cosmpy.aerial.config.NetworkConfig.chain4energy_beta_testnet"></a>

#### chain4energy`_`beta`_`testnet

```python
@classmethod
def chain4energy_beta_testnet(cls)
```

Get the Chain4energy beta testnet.

**Raises**:

- `RuntimeError`: No beta testnet available

<a id="cosmpy.aerial.config.NetworkConfig.chain4energy_stable_testnet"></a>

#### chain4energy`_`stable`_`testnet

```python
@classmethod
def chain4energy_stable_testnet(cls)
```

Get the Chain4energy stable testnet.

**Returns**:

Chain4energy stable testnet. For now veles is Chain4energy stable testnet.

<a id="cosmpy.aerial.config.NetworkConfig.chain4energy_mainnet"></a>

#### chain4energy`_`mainnet

```python
@classmethod
def chain4energy_mainnet(cls) -> "NetworkConfig"
```

Get the chain4energy mainnet configuration.

**Returns**:

C4E mainnet configuration

<a id="cosmpy.aerial.config.NetworkConfig.latest_stable_testnet"></a>

#### latest`_`stable`_`testnet

```python
@classmethod
def latest_stable_testnet(cls) -> "NetworkConfig"
```

Get the latest stable testnet.

**Returns**:

latest stable testnet

