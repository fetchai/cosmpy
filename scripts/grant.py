from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.contract import create_cosmwasm_execute_msg
from cosmpy.aerial.tx import SigningCfg, Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


ALICE = "c91cdb3cedafbc7fdf226ce033ca6139977bbc456e3431642387c2d383825fbc"
# BOB = "30e8ef360bf8d625d3fb674eb49a616dd302b28c1fa3bccd4621e8864ae20ad1"
BOB = "df0eb7985d3e5e7c49ddd35e000ff1eb5ac3c808909766d41cedfde99503f059"

alice = LocalWallet(PrivateKey(bytes.fromhex(ALICE)))
alice_sequence = 1
alice_account_number = 90398

bob = LocalWallet(PrivateKey(bytes.fromhex(BOB)))
bob_account_number = None  # 90431
bob_sequence = 0

client = LedgerClient(NetworkConfig.fetchai_stable_testnet())

contract_address = "fetch1kskk44akt3uwr3umnxhgyxet7nmrhdlf2gyyqaw5snxm0qx8ud7qgxwkds"

msg = {"set": {"value": "foobar"}}

tx = Transaction()
tx.add_message(
    create_cosmwasm_execute_msg(bob.address(), contract_address, msg, funds=None)
)

# we need to build up a representative transaction so that we can accurately simulate it
tx.seal(
    [
        SigningCfg.direct(bob.public_key(), bob_sequence),
        SigningCfg.direct(alice.public_key(), alice_sequence),
    ],
    fee="",
    gas_limit=0,
    memo="",
    fee_payer=alice.address(),
)
tx.sign(bob.signer(), client.network_config.chain_id, bob_account_number)
tx.sign(alice.signer(), client.network_config.chain_id, alice_account_number)
tx.complete()


# simulate the gas and fee for the transaction
# gas_limit, fee = client.estimate_gas_and_fee_for_tx(tx)

# finally, build the final transaction that will be executed with the correct gas and fee values
tx.seal(
    [
        SigningCfg.direct(bob.public_key(), bob_sequence),
        SigningCfg.direct(alice.public_key(), alice_sequence),
    ],
    fee="6000000000000000atestfet",
    gas_limit=6000000,
    memo="",
    fee_payer=alice.address(),
)

tx.sign(bob.signer(), client.network_config.chain_id, bob_account_number)
tx.sign(alice.signer(), client.network_config.chain_id, alice_account_number)
tx.complete()


client.broadcast_tx(tx)
