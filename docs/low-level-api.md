The Cosmpy library provides a high-level API which greatly simplifies the
most common use cases when interacting with Cosmos-based chains (e.g. [sending
tokens](send-tokens.md), [staking](staking.md), [deploying and interacting with contracts](deploy-a-contract.md)). There are [documentation](connect-to-network.md) and
[example code](https://github.com/fetchai/cosmpy/tree/master/examples) covering such use cases.

However, cosmpy also provides low-level access to the entire Cosmos-SDK, enabling the
full gamut of functionality to be accessed, albeit with a little more boiler-plate.

Here, we aim to help developers navigate the low-level, protobuf-based API functionality, provided by Cosmpy.

## Recap: High Level API - Aerial

As a reminder, here is a quick example of using the high level functionality provided by Cosmpy. In this case, we connect to a testnet, create a wallet, stake some tokens with a validator, then claim our rewards:

```python
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())
wallet = LocalWallet(PrivateKey("rBDA3Q0vK5T+JVQmXSoooqUY/mSO4mmhMHQJI31+h1o="))
tx = client.delegate_tokens("fetchvaloper1rsane988vksrgp2mlqzclmt8wucxv0ej4hrn2k", 20, wallet)
tx.wait_to_complete()
tx = client.claim_rewards("fetchvaloper1rsane988vksrgp2mlqzclmt8wucxv0ej4hrn2k", wallet)
tx.wait_to_complete()
```

The available high-level helper functions provided by cosmpy can be found by browsing for instance
[the aerial client package](https://github.com/fetchai/cosmpy/blob/master/cosmpy/aerial/client/__init__.py).

## Low Level API

### Simple Messages

Not all Cosmos-SDK functionality is encapsulated in the high level aerial packages. In which case, it is necessary to locate and use the definition of the relevant protobuf message.

Analogous to the rewards claim example above, what if a validator operator wanted to claim their commission? At the time of writing, there is no high-level API to achieve this, so the low level API must be used.

In the [protos](https://github.com/fetchai/cosmpy/tree/master/cosmpy/protos) directory, there is a [MsgWithdrawValidatorCommission](https://github.com/fetchai/cosmpy/blob/6d7b5f49722b67c803145d55aa291fe426c19994/cosmpy/protos/cosmos/distribution/v1beta1/tx_pb2.py#L160)
message, which is what we need. It takes a single `validator_address` parameter which is a `utf-8` string.

To send a transaction containing such a message:

```python
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.protos.cosmos.distribution.v1beta1.tx_pb2 import MsgWithdrawValidatorCommission
from cosmpy.crypto.keypairs import PrivateKey

client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())
wallet = LocalWallet(PrivateKey("<redacted>private key of dorado validator0"))

tx = Transaction()
tx.add_message(
    MsgWithdrawValidatorCommission(
        validator_address="fetchvaloper1rsane988vksrgp2mlqzclmt8wucxv0ej4hrn2k"
    )
)
tx = prepare_and_broadcast_basic_transaction(client, tx, wallet)
tx.wait_to_complete()
```

### Nested messages

The above example creates and broadcasts a simple `MsgWithdrawValidatorCommission` message. However, sometimes it is necessary to include one message in another. For example, what if we wanted to use the above message but execute it from a different account using `authz` (i.e. use an account which holds minimal funds, whose keys need not be treated with the same level of care as those of the validator itself)?

In this case, we'll need to send an `authz`
[MsgExec](https://github.com/fetchai/cosmpy/blob/4abb976753edcab402fcc23d4dce3ab67b73b608/cosmpy/protos/cosmos/authz/v1beta1/tx_pb2.py#L114)
message, which can be found in [tx_pb2.py](https://github.com/fetchai/cosmpy/blob/4abb976753edcab402fcc23d4dce3ab67b73b608/cosmpy/protos/cosmos/authz/v1beta1/tx_pb2.py) under `cosmos/authz` area of `cosmpy/protos`.
This message takes two parameters. The `grantee` is a simple string address similar to the above. But the `msgs` field needs to support multiple types of messages and not just `MsgWithdrawValidatorCommission`.

Protobuf is strongly typed, so to facilitate this flexibility, it is necessary to first pack the nested message into a `protobuf.Any` message.

Therefore, we arrive at the code looking like:

```python
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.distribution.v1beta1.tx_pb2 import MsgWithdrawValidatorCommission
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgExec
from google.protobuf import any_pb2

client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())
wallet = LocalWallet(PrivateKey("rBDA3Q0vK5T+JVQmXSoooqUY/mSO4mmhMHQJI31+h1o="))

msg = any_pb2.Any()
msg.Pack(
    MsgWithdrawValidatorCommission(
        validator_address="fetchvaloper1rsane988vksrgp2mlqzclmt8wucxv0ej4hrn2k"
    ),
    "",
)

tx = Transaction()
tx.add_message(MsgExec(grantee=str(wallet.address()), msgs=[msg]))

tx = prepare_and_broadcast_basic_transaction(client, tx, wallet)
tx.wait_to_complete()
```

### More protobuf examples

Before running the above, the necessary `authz` grant must first be put in place. For Ledger Nano users (other hardware wallets are also available) that might mean an excursion to the command line. For the Fetchai network using [FetchD](https://docs.fetch.ai/ledger_v2/):

```bash
fetchd tx authz grant $(fetchd keys show grantee --output json | jq -r .address) generic --msg-type "/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission" --from=$(fetchd keys show grantor --output json | jq -r .address) --gas auto --gas-adjustment 1.5 --gas-prices 5000000000atestfet
```

By default, the above provides one year's worth of authorization to withdraw validator commission using accounts already present in the keyring.

For those with access to their keys in python:

```python
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.distribution.v1beta1.tx_pb2 import MsgWithdrawValidatorCommission
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgGrant
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import GenericAuthorization, Grant

from google.protobuf import any_pb2, timestamp_pb2
from datetime import datetime, timedelta

client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())
wallet = LocalWallet(PrivateKey("rBDA3Q0vK5T+JVQmXSoooqUY/mSO4mmhMHQJI31+h1o="))
validator = LocalWallet(PrivateKey("<redacted>private key of dorado validator0"))

authz_any = any_pb2.Any()
authz_any.Pack(
    GenericAuthorization(
        msg="/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission"
    ),
    "",
)

expiry = timestamp_pb2.Timestamp()
expiry.FromDatetime(datetime.now() + timedelta(seconds=60))
grant = Grant(authorization=authz_any, expiration=expiry)

msg = MsgGrant(
    granter=str(validator.address()),
    grantee=str(wallet.address()),
    grant=grant,
)

tx = Transaction()
tx.add_message(msg)

tx = prepare_and_broadcast_basic_transaction(client, tx, validator)
tx.wait_to_complete()
```
