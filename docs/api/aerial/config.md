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

<a id="cosmpy.aerial.config.NetworkConfig.fetchai_dorado_testnet"></a>

#### fetchai`_`dorado`_`testnet

```python
@classmethod
def fetchai_dorado_testnet(cls) -> "NetworkConfig"
```

Fetchai dorado testnet.

**Returns**:

Network configuration

<a id="cosmpy.aerial.config.NetworkConfig.asi_eridanus_testnet"></a>

#### asi`_`eridanus`_`testnet

```python
@classmethod
def asi_eridanus_testnet(cls) -> "NetworkConfig"
```

ASI Eridanus testnet.

**Returns**:

Network configuration

<a id="cosmpy.aerial.config.NetworkConfig.fetchai_alpha_testnet"></a>

#### fetchai`_`alpha`_`testnet

```python
@classmethod
def fetchai_alpha_testnet(cls)
```

Get the fetchai alpha testnet.

**Raises**:

- `RuntimeError`: No alpha testnet available

<a id="cosmpy.aerial.config.NetworkConfig.fetchai_beta_testnet"></a>

#### fetchai`_`beta`_`testnet

```python
@classmethod
def fetchai_beta_testnet(cls)
```

Get the Fetchai beta testnet.

**Raises**:

- `RuntimeError`: No beta testnet available

<a id="cosmpy.aerial.config.NetworkConfig.fetchai_stable_testnet"></a>

#### fetchai`_`stable`_`testnet

```python
@classmethod
def fetchai_stable_testnet(cls)
```

Get the fetchai stable testnet.

**Returns**:

fetchai stable testnet. For now dorado is fetchai stable testnet.

<a id="cosmpy.aerial.config.NetworkConfig.fetchai_mainnet"></a>

#### fetchai`_`mainnet

```python
@classmethod
def fetchai_mainnet(cls) -> "NetworkConfig"
```

Get the fetchai mainnet configuration.

**Returns**:

fetch mainnet configuration

<a id="cosmpy.aerial.config.NetworkConfig.fetch_mainnet"></a>

#### fetch`_`mainnet

```python
@classmethod
def fetch_mainnet(cls) -> "NetworkConfig"
```

Get the fetch mainnet.

**Returns**:

fetch mainnet configurations

<a id="cosmpy.aerial.config.NetworkConfig.latest_stable_testnet"></a>

#### latest`_`stable`_`testnet

```python
@classmethod
def latest_stable_testnet(cls) -> "NetworkConfig"
```

Get the latest stable testnet.

**Returns**:

latest stable testnet

