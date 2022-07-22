To start interacting with a blockchain, you first need to establish a connection to a network node. You can use `LedgerClient` as a client object which takes a `NetworkConfig` as an argument.

```python
from cosmpy.aerial.client import LedgerClient, NetworkConfig

ledger_client = LedgerClient(NetworkConfig.fetch_mainnet())
```

For convenience, some networks' configurations are provided automatically. For example, `NetworkConfig.fetch_mainnet()` is the configuration for the Fetch ledger. If you want to interact with other chains, you can customise `NetworkConfig` as shown in the example below:

```python
cfg = NetworkConfig(
    chain_id="cosmoshub-4",
    url="grpc+https://grpc-cosmoshub.blockapsis.com:429",
    fee_minimum_gas_price=1,
    fee_denomination="uatom",
    staking_denomination="uatom",
)

ledger_client = LedgerClient(cfg)
```

A full list of chain identifiers, denominations and end-points can be found at the Cosmos [chain registry](https://github.com/cosmos/chain-registry/).

