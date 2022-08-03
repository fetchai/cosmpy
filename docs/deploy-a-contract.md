You can deploy smart contracts in CosmPy using `LedgerContract`. For this, you will need the path to where the contract is stored (in this case `simple.wasm`), a [`LedgerClient`](connect-to-network.md) and a [`Wallet`](wallets-and-keys.md):

```python
from cosmpy.aerial.contract import LedgerContract

PATH = "../simple.wasm"

contract = LedgerContract(PATH, ledger_client)
contract.deploy({}, wallet)
```

You can now start interacting with the contract. To get the address of where the contract is deployed on the network:

```python
print(f"Contract deployed at: {contract.address}")
```

You can query the values of the contract's state variables: 

```python
result = contract.query({"get": {"owner": wallet}})
print("Initial state:", result)
```

You can also set these values. The following sets the state variable `value` to `foobar`:

```python
contract.execute({"set": {"value": "foobar"}}, wallet).wait_to_complete()
```

Let's check if this was set correctly:

```python
result = contract.query({"get": {"owner": wallet)}})
print("State after set:", result)
```

Similarly, you can clear the state variables:

```python
contract.execute({"clear": {}}, wallet).wait_to_complete()

result = contract.query({"get": {"owner": wallet}})
print("State after clear:", result)
```
