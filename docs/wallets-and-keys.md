# Wallets and Keys

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