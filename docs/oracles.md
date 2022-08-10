**Oracles** are entities that can update state variables in smart contracts and whose goal is usually to accurately estimate or predict some real world quantity or quantities. These quantities can then be used in the logic of other smart contracts.

This guide shows how to write a CosmPy script that deploys and updates an oracle contract with a coin price, and another script that deploys a contract that queries this coin price.

## Preliminaries

We will need the binaries for both contracts, which can be downloaded as follows:
```bash
wget https://raw.githubusercontent.com/fetchai/agents-aea/develop/packages/fetchai/contracts/oracle/build/oracle.wasm
wget https://raw.githubusercontent.com/fetchai/agents-aea/develop/packages/fetchai/contracts/oracle_client/build/oracle_client.wasm
```

The scripts also require the following imports:
```python
from time import sleep
import requests
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
```

## Oracle deployer and updater

We first choose a data source for the coin price, the update interval, and the decimal precision for the oracle value:
```python
COIN_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=fetch-ai&vs_currencies=usd"
)
UPDATE_INTERVAL_SECONDS = 10
ORACLE_VALUE_DECIMALS = 5
```

Next, we create a wallet and ledger interface to interact with the latest stable testnet:
```python
wallet = LocalWallet(PrivateKey("T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))
ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
```

Create the `LedgerContract` object:
```python
contract = LedgerContract("oracle.wasm", ledger)
```

To deploy the oracle contract, add the fee amount to the instantiation message and call the deploy function:
```python
instantiation_message = {"fee": "100"}
contract.deploy(instantiation_message, wallet, funds="1atestfet")
print(f"Oracle contract deployed at: {contract.address}")
```

Save the oracle contract address to use for the oracle client script below (`ORACLE_CONTRACT_ADDRESS`).

As the deployer of the contract, we have permission to grant the oracle to a particular address.
In this case, we'll grant the oracle role to our own wallet:
```python
grant_role_message = {"grant_oracle_role": {"address": wallet)}}
contract.execute(grant_role_message, wallet).wait_to_complete()
```

Finally, start updating the contract with the coin price retrieved from the `COIN_PRICE_URL`:
```python
while True:
    resp = requests.get(COIN_PRICE_URL).json()
    price = resp["fetch-ai"]["usd"]
    value = int(price * 10**ORACLE_VALUE_DECIMALS)
    update_message = {
        "update_oracle_value": {
            "value": str(value),
            "decimals": str(ORACLE_VALUE_DECIMALS),
        }
    }
    contract.execute(update_message, wallet).wait_to_complete()
    print(f"Oracle value updated to: {price} USD")
    print(f"Next update in {UPDATE_INTERVAL_SECONDS} seconds...")
    sleep(UPDATE_INTERVAL_SECONDS)
```

For the complete example script, see [aerial_oracle.py](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_oracle.py).

## Oracle client

Now we'll write a script that deploys a contract that can request the oracle value in exchange for the required fee.

We again start by creating a wallet and ledger interface in a new terminal session:
```python
wallet = LocalWallet(PrivateKey("CI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8="))
ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
```

Set `ORACLE_CONTRACT_ADDRESS` to the address of the contract deployed in the previous script:
```python
ORACLE_CONTRACT_ADDRESS = "contract_address_goes_here"
```

Next, we define the contract object, set the oracle contract address in the instantiation message, and deploy the contract:
```python
contract = LedgerContract("oracle_client.wasm", ledger)
instantiation_message = {"oracle_contract_address": str(ORACLE_CONTRACT_ADDRESS)}
contract.deploy(instantiation_message, wallet)
```

Finally, define a request interval and start a loop that executes the function that requests the oracle value:
```python
REQUEST_INTERVAL_SECONDS = 10
while True:
    request_message = {"query_oracle_value": {}}
    contract.execute(
        request_message, wallet, funds="100atestfet"
    ).wait_to_complete()
    result = contract.query({"oracle_value": {}})
    print(f"Oracle value successfully retrieved: {result}")
    sleep(REQUEST_INTERVAL_SECONDS)
```

For the complete example script, see [aerial_oracle_client.py](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_oracle_client.py).