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

## Exporting private keys from your CLI keyring

If you wish to use cosmpy with an account already present in your CLI keyring, extract the private key and convert it into a base64 encoded string as follows (using the fetchd CLI
as an example)...

```bash
fetchd keys export mykeyname --unsafe --unarmored-hex | xxd -r -p | base64
```

## Recovering keys from a mnemonic, using python

If you wish to use cosmpy with an account for which you have the mnemonic phrase, although you
could always add it to your fetchd keyring then export it as above, it is also possible to
achieve this in python as follows...

```python
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

mnemonic = "person knife december tail tortoise jewel warm when worry limit reward memory piece cool sphere kitchen knee embody soft own victory sauce silly page"
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()))
```

(Obviously, in real life, you would _never_ include a mnemonic in code that is checked in to git!)
