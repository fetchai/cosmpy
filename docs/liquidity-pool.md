## Swap Tokens

You can interact with a liquidity pool by swapping atestfet for CW20 tokens or vice versa.
First, perform all the necessary imports:

```python
import base64
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet
```
Set the network configuration, define a local wallet and add some tokens to it using the FaucetApi

```python
# Network configuration
ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

# Define any wallet
wallet = LocalWallet.generate()

# Add tokens to wallet
faucet_api = FaucetApi(NetworkConfig.latest_stable_testnet())
faucet_api.get_wealth(wallet.address())
```
Define the CW20, pair, and liquidity token contracts with the following addresses:

```python
# Define cw20, pair and liquidity token contracts
token_contract_address = (
    "fetch1qr8ysysnfxmqzu7cu7cq7dsq5g2r0kvkg5e2wl2fnlkqss60hcjsxtljxl"
)
pair_contract_address = (
    "fetch1vgnx2d46uvyxrg9pc5mktkcvkp4uflyp3j86v68pq4jxdc8j4y0s6ulf2a"
)
liq_token_contract_address = (
    "fetch1alzhf9yhghud3qhucdjs895f3aek2egfq44qm0mfvahkv4jukx4qd0ltxx"
)

token_contract = LedgerContract(
    path=None, client=ledger, address=token_contract_address
)
pair_contract = LedgerContract(
    path=None, client=ledger, address=pair_contract_address
)
liq_token_contract = LedgerContract(
    path=None, client=ledger, address=liq_token_contract_address
)
```

Swap the defined `swap_amount`of atestfet for CW20 tokens

```python
# Swap atestfet for CW20 tokens
swap_amount = "10000"
native_denom = "atestfet"

tx = pair_contract.execute(
    {
        "swap": {
            "offer_asset": {
                "info": {"native_token": {"denom": native_denom}},
                "amount": swap_amount,
            }
        }
    },
    sender=wallet,
    funds=swap_amount + native_denom,
)
tx.wait_to_complete()
```

You can query your CW20 balance using the following code:

```python
token_contract.query({"balance": {"address": str(wallet.address())}})
```

To trade 10 CW20 tokens for atestfet you can use the following:

```python
tx = token_contract.execute({
  "send": {
    "contract": pair_contract_address,
    "amount": "10",
    "msg": "eyJzd2FwIjp7fX0="
  }
},wallet)

tx.wait_to_complete()
```
## Add and Remove Liquidity 

You need to increase your wallet's allowance to provide CW20 tokens to the liquidity pool. You dont need to increase the allowance to provide atestfet

```python
# Set the amount of CW20 tokens to be added to liquidity pool
cw20_liquidity_amount = "100"

# Increase allowance
tx = token_contract.execute(
    {
        "increase_allowance": {
            "spender": pair_contract_address,
            "amount": cw20_liquidity_amount,
            "expires": {"never": {}},
        }
    },
    wallet,
)

tx.wait_to_complete()
```
To set the amount of atestfet to be added to the liquidity pool and not influence the existing token prices, we need to choose an amount that matches the atestfet:CW20 token ratio already existing in the pool. For this reason, we will query the `pair_contract` pool to observe the atestfet:CW20 token ratio

```python
# Query Liquidity Pool
pair_contract.query({"pool": {}})
```

At the moment the code was run, the ratio was close to 247:10 atestfet:CW20, and since we defined above the amount of CW20 tokens to provide to the liquidity pool as 100, we will match the LP pool ratio by setting the atestfet amount as 2470. It will be difficult to exactly match the current ratio of the pool, but when adding liquidity to the pool, there is a slippage_tolerance parameter that allows a certain percentage change in the price.

```python
# Set the amount of atestfet tokens to be added to liquidity pool
native_liquidity_amount = "2470"

# Provide Liquidity
# Liquidity should be added so that the slippage tolerance parameter isn't exceeded

tx = pair_contract.execute(
    {
        "provide_liquidity": {
            "assets": [
                {
                    "info": {"token": {"contract_addr": token_contract_address}},
                    "amount": cw20_liquidity_amount,
                },
                {
                    "info": {"native_token": {"denom": native_denom}},
                    "amount": native_liquidity_amount,
                },
            ],
        "slippage_tolerance":"0.1"
        }
    },
    sender=wallet,
    funds=native_liquidity_amount + native_denom,
)

tx.wait_to_complete()
```

When providing liquidity, you are rewarded with newly minted LP tokens. LP tokens represent the liquidity provider's share in the pool. You can burn your LP tokens to withdraw your share from the liquidity pool, for more information visit [`Terraswap`](https://docs.terraswap.io/). The following code shows how to withdraw your share from the LP.

```python
# Query your LP token balance to burn it all
LP_token_balance = liq_token_contract.query({"balance": {"address": str(wallet.address())}})["balance"]

# Convert the withdraw msg to base64
withdraw_msg = '{"withdraw_liquidity": {}}'
withdraw_msg_bytes = withdraw_msg.encode("ascii")
withdraw_msg_base64 = base64.b64encode(withdraw_msg_bytes)
msg = str(withdraw_msg_base64)[2:-1]

# Withdraw Liquidity
tx = liq_token_contract.execute(
    {
        "send": {
            "contract": pair_contract_address,
            "amount": LP_token_balance,
            "msg": msg,
        }
    },
    sender=wallet,
)

tx.wait_to_complete()
```

You can now query you LP token balance to observe that it has gone down to zero

```python
liq_token_contract.query({"balance": {"address": str(wallet.address())}})
```

You can also check the full code example at [`liquidity-pool`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_liquidity_pool.py)