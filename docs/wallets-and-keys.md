To make changes on a network, you will need to start sending transactions to it. This in tern involves managing private keys and addresses. Luckily, CosmPy makes this relatively straightforward.

The following code outlines how to both generate a completely new private key and how to recover a previously generated one:

```python
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# To create a random private key:
private_key = PrivateKey()

# To recover an existing private key:
private_key = PrivateKey('<base64 encoded private key>')
```

The `PrivateKey` object is one of CosmPy's low level primitives. This is why it is generally paired with a `Wallet` object in most scenarios. Below, a `LocalWallet` (a kind of `Wallet`) is created using the private key:

```python
wallet = LocalWallet(private_key)
```

Creating the wallet allows users to query useful information such as the address from the wallet directly.

```python
print(wallet.address()) # will print the address for the wallet
```

## Existing account

To use CosmPy with an existing account, extract the private key and convert it into a base64 encoded string.

For example, to do this on macOS or Linux for the Fetch.ai network using its [FetchD](https://network.fetch.ai/docs/guides/cosmpy/creating-wallet/) CLI:

```bash
fetchd keys export mykeyname --unsafe --unarmored-hex | xxd -r -p | base64
```

### From mnemonic

If you have the mnemonic phrase to an account, you can get the associated private key as follows:

```python
from cosmpy.mnemonic import derive_child_key_from_mnemonic
from cosmpy.aerial.wallet import LocalWallet, PrivateKey

mnemonic = "person knife december tail tortoise jewel warm when worry limit reward memory piece cool sphere kitchen knee embody soft own victory sauce silly page"
private_key = derive_child_key_from_mnemonic(mnemonic)

wallet = LocalWallet(PrivateKey(private_key))
```

!!! danger
    Of course in real applications, you should **never** include a mnemonic in public code.


### Custom prefix network:
In case you are using a network other than fetch.ai's, you can provide the custom prefix when creating the wallet:

```
alice = LocalWallet(PrivateKey("L1GsisFk+oaIug3XZlILWk2pJDVFS5aPJsrovvUEDrE="), prefix="custom_prefix")
address = alice.address()
print(f"Address: {address}")
balance = client.query_bank_balance(address, "uatom")
```
