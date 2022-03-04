from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# Denomination and amount of transferred tokens
DENOM = "atestfet"
AMOUNT = [Coin(amount="1", denom=DENOM)]

# Node config
REST_ENDPOINT_ADDRESS = "https://rest-capricorn.fetch.ai:443"
FAUCET_URL = "https://faucet-capricorn.t-v2-london-c.fetch-ai.com"
CHAIN_ID = "capricorn-1"
PREFIX = "fetch"
MINIMUM_GAS_PRICE = Coin(denom=DENOM, amount=str(500000000000))

sender_crypto = CosmosCrypto(prefix=PREFIX)
receiver_crypto = CosmosCrypto(prefix=PREFIX)

# Create ledger
ledger = CosmosLedger(
    chain_id=CHAIN_ID,
    rest_node_address=REST_ENDPOINT_ADDRESS,
    minimum_gas_price=MINIMUM_GAS_PRICE,
    faucet_url=FAUCET_URL,
)

# Refill sender's balance from faucet
ledger.ensure_funds([sender_crypto.get_address()])

# Print balance before transfer
print("Before transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Sender has {res} {DENOM}")
res = ledger.get_balance(receiver_crypto.get_address(), DENOM)
print(f"Receiver has {res} {DENOM}")

# Generate, sign and broadcast send tokens transaction
ledger.send_funds(sender_crypto, receiver_crypto.get_address(), AMOUNT)

# Print balance after transfer
print("After transaction")
res = ledger.get_balance(sender_crypto.get_address(), DENOM)
print(f"Sender has {res} {DENOM}")
res = ledger.get_balance(receiver_crypto.get_address(), DENOM)
print(f"Receiver has {res} {DENOM}")
