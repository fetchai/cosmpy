A mean-reversion strategy expects the prices to return to “normal” levels or a certain moving average following a temporary price spike. We can construct a similar strategy using the Liquidity Pool, where we will set upper and lower bound prices that will trigger a sell and a buy transaction respectively. If the behavior of the LP prices works as expected always returning to a certain moving average, we could profit by selling high and buying low. We will do this by swapping atestfet and CW20 with the Liquidity Pool, we refer to a sell transaction when we sell atestfet and get CW20 tokens, a buy transaction would be exactly the oposite.

The code will require the following imports:

```python
from time import sleep
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet
```

We will define the *swap_native_for_cw20* function that trades `swap_amount` of atestfet from `wallet` for CW20 tokens by executing a `pair_contract`:


```python
def swap_native_for_cw20(swap_amount, pair_contract, wallet):
    tx = pair_contract.execute({
      "swap": {
        "offer_asset": {
          "info": {
            "native_token": {
              "denom": "atestfet"
            }
          },
          "amount": str(swap_amount)
        }
      }
    },sender= wallet, funds= str(swap_amount) + "atestfet")
    print("swapping native for cw20 tokens")
    tx.wait_to_complete()
```
Now, we will define the *swap_cw20_for_native* function that does exactly the opposite of the function defined above: trades `swap_amount` of CW20 tokens from `wallet` for atestfet. This time the CW20 `token_contract` is executed using the `pair_contract_address`. Finally you need to include the {"swap":{}} message in the "msg" field. However, this swap message has to be encoded into base64. When you encode {"swap":{}} message into base64 you get: eyJzd2FwIjp7fX0=

```python
def swap_cw20_for_native(swap_amount, pair_contract_address, token_contract, wallet):
    tx = token_contract.execute({
      "send": {
        "contract": pair_contract_address,
        "amount": str(swap_amount),
        "msg": "eyJzd2FwIjp7fX0="
      }
    },wallet)
    print("swapping cw20 for native tokens")
    tx.wait_to_complete()
```
Set the network configuration, define a local wallet and add some tokens to it using the FaucetApi

```python
# Define any wallet
wallet =  LocalWallet.generate()

# Network configuration
ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

# Add tokens to wallet
faucet_api = FaucetApi(NetworkConfig.latest_stable_testnet())
wallet_balance = ledger.query_bank_balance(wallet.address())

while wallet_balance < (10**18):
    print("Providing wealth to wallet...")
    faucet_api.get_wealth(wallet.address())
    wallet_balance = ledger.query_bank_balance(wallet.address())

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

We will define a trading wallet named `tokens` that will keep track of the amount of atestfet or CW20 tokens we hold at each moment. The `currency` variable will keep track of the token type. We will never have a mixed trading wallet since in this strategy, every time we perform a swap, we sell all the current tokens.

```python
# Trading Wallet
tokens = 1000000
currency = "atestfet"
```

Now we will define the upper and lower price bounds (atestfet/CW20) that will trigger a buy and a sell transaction of atestfet. We also define the commission rate (0.3% in [`Terraswap`](https://docs.terraswap.io/docs/introduction/trading_fees/)) and the `interval` time step to query the pool's price.

```python
upper_bound = 26
lower_bound = 24


# LP commission
commission = 0.003

# Interval in seconds
interval = 5
```
Finally, we will initialize a loop, in every step it will:

* Query the Liquidity Pool status
* Check if current trading wallet's `currency`
* Calculate the *atestfet/CW20* price using the tokens received `tokens_out` if the whole trading wallet's balance `tokens` was to be swapped with the liquidity pool
* If atestfet sell/buy price is equal or lower/higher than the lower/upper bound, it will trigger a sell/buy transaction of atestfet to buy/sell CW20 tokens.
* Update trading wallet `token` balance and `currency`
* Sleep `interval` and repeat

```python
while True:
    
    # Query LP status
    pool = pair_contract.query({"pool": {}})
    native_amount = int(pool["assets"][1]["amount"])
    cw20_amount = int(pool["assets"][0]["amount"])

    if currency == "atestfet":
        # Calculate received tokens if tokens amount is given to LP
        tokens_out = round(((cw20_amount*tokens)/(native_amount+tokens))*(1-commission))
        
        # Sell price of atestfet => give atestfet, get cw20
        sell_price = tokens/tokens_out
        print("atestfet sell price: ", sell_price)
        if sell_price <= lower_bound:
            swap_native_for_cw20(tokens, pair_contract, wallet)
            tokens = int(token_contract.query({"balance": {"address": str(wallet.address())}})["balance"])
            currency = "CW20"
    else:
        # Calculate received tokens if tokens amount is given to LP
        tokens_out = round(((native_amount*tokens)/(cw20_amount+tokens))*(1-commission))
        
        # Buy price of atestfet => give cw20, get atestfet
        buy_price = tokens_out/tokens
        print("atestfet buy price: ", buy_price)
        if buy_price >= upper_bound:
            swap_cw20_for_native(tokens, pair_contract_address, token_contract, wallet)
            tokens = tokens_out
            currency = "atestfet"

    sleep(interval)
```

This code assumes other traders performing transactions with the Liquidity Pool that will generate price movements.
You can check out the full example at [`swap-automation`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_swap_automation.py)