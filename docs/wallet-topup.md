In a case where you are performing multiple transactions from a certain task_wallet, you can set an algorithm to keep that wallet address topped-up. For this use case, we will use three different wallets: wallet, authz_wallet, and task_wallet. Wallet will be the main wallet address that we don't want to give full access to, therefore we will authorize authz_wallet to send a certain amount of tokens from wallet to task_wallet every time task_wallet balance falls below a certain `minimum_balance` threshold. This way, task_wallet can keep performing transactions using the main wallet's tokens by being topped-up by authz_wallet. Start by defining wallet, authz_wallet and task_wallet address.

```python
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.aerial.client import LedgerClient, NetworkConfig

ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

# Define wallets with any private keys
wallet = LocalWallet(PrivateKey("F7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))

authz_wallet = LocalWallet(
    PrivateKey("KI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=")
)

# Define any task_wallet address
task_wallet_address = 'fetch1ay6grfwhlm00wydwa3nw0x2u44qz4hg2uku8dc'
```
Wallet will need to have enough tokens available to top-up task_wallet, and authz_wallet will need enough tokens to pay for transaction fees. Now you will need to give authorization to authz_wallet to send tokens from wallet. You will define the expiration and the spend limit of the authorization in `total_authz_time` and `spend_amount`. The code below shows how to perform this kind of transaction:

```python
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction

from datetime import datetime, timedelta

from google.protobuf import any_pb2, timestamp_pb2
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import Grant
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgGrant
from cosmpy.protos.cosmos.bank.v1beta1.authz_pb2 import SendAuthorization

# Set total authorization time and spend amount
total_authz_time = 10000
amount = 1000000000000000000
spend_amount = Coin(amount=str(amount), denom="atestfet")

# Authorize authz_wallet to send tokens from wallet
authz_any = any_pb2.Any()
authz_any.Pack(
    SendAuthorization(spend_limit=[spend_amount]),
    "",
)

expiry = timestamp_pb2.Timestamp()
expiry.FromDatetime(datetime.now() + timedelta(seconds=total_authz_time * 60))
grant = Grant(authorization=authz_any, expiration=expiry)

msg = MsgGrant(
    granter=str(wallet.address()),
    grantee=str(authz_wallet.address()),
    grant=grant,
)

tx = Transaction()
tx.add_message(msg)

tx = prepare_and_broadcast_basic_transaction(ledger, tx, wallet)
tx.wait_to_complete()
```

Next, you will need to define the amount to top-up, the threshold that will trigger the top-up, and the interval time to query the task_wallet balance. We will define these amounts in the following variables: `top_up_amount`, `minimum_balance` and `interval_time`.

```python

# Top-up amount
amount = 10000000000000000
top_up_amount = Coin(amount=str(amount), denom="atestfet")

# Minimum balance for task_wallet
minimum_balance = 1000000000000000

# Interval to query task_wallet's balance in seconds
interval_time = 5
```

Finally, run a continuously running loop that will:
* Check the main wallet's balance to make sure it has enough tokens to top-up the task_wallet_address
* Check task_wallet's balance, if it is lower than `minimum_balance` then authz_wallet will send `top_up_amount` of tokens from wallet to task_wallet
* Sleep `interval_time` and repeat

```python
import time
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgExec
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend

while True:

    wallet_address = str(wallet.address())

    wallet_balance = ledger.query_bank_balance(wallet_address)

    if wallet_balance < amount:
        print("Wallet doesn't have enough balance to top-up task_wallet")
        break

    task_wallet_balance = ledger.query_bank_balance(task_wallet_address)

    if task_wallet_balance < minimum_balance:

        print("topping up task wallet")
        # Top-up task_wallet
        msg = any_pb2.Any()
        msg.Pack(
            MsgSend(
                from_address=wallet_address,
                to_address=task_wallet_address,
                amount=[top_up_amount],
            ),
            "",
        )

        tx = Transaction()
        tx.add_message(MsgExec(grantee=str(authz_wallet.address()), msgs=[msg]))

        tx = prepare_and_broadcast_basic_transaction(ledger, tx, authz_wallet)
        tx.wait_to_complete()

    time.sleep(interval_time)
```

While the code above keeps running, you can make sure that task_wallet is always topped-up as long as authz_wallet has authorization to send the required tokens and the main wallet has enough balance.

You can also check out the authorization and top-up code examples at [`authz`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_authz.py) and [`top-up`](https://github.com/fetchai/cosmpy/blob/develop/examples/aerial_topup.py) respectively.



