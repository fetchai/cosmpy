# Cosmpy - Low level API examples

The Cosmpy library provides a high level API which greatly simplifies the
most common use cases when interacting with Cosmos based chains (sending
tokens, staking, deploying and interacting with contracts etc). This repo contains
[documentation](https://github.com/fetchai/cosmpy/blob/master/docs/) and
[example code](https://github.com/fetchai/cosmpy/tree/master/examples) covering
the use of Cosmpy for such use cases.

However it also provides low-level access to the entire Cosmos SDK, enabling the
full gamut of functionality to be accessed, albeit with a little more boiler-plate.

This document is intended to help developers navigate the low-level, protobuf based API functionality, provided by Cosmpy.

## Recap: High Level API - Aerial

As a reminder, here is a quick example of using the high level functionality
provided by Cosmpy. In this case, we connect to a testnet, create a wallet,
stake some tokens with a validator, then claim our rewards...

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

The available high-level helper functions provided by Cosmpy can be found by browsing eg
[the aerial client package]("https://github.com/fetchai/cosmpy/blob/master/cosmpy/aerial/client/__init__.py").

## Low Level API - simple messages

However, not all cosmos-sdk functionality is encapsulated in the high level aerial packages.
In which case it is necessary to locate, and use, the definition of the relevant protobuf message.

For example, analagous to the reward claim example given above, what if a validator operator
wished to claim their commission? Now, at the time of writing, there is no
`client.claim_commission()` high level API method available, so the low level API
must be used.

Drilling down into the [protos](cosmpy/cosmpy/protos/) directory, we come across the definition
of a [MsgWithdrawValidatorCommission](https://github.com/fetchai/cosmpy/blob/6d7b5f49722b67c803145d55aa291fe426c19994/cosmpy/protos/cosmos/distribution/v1beta1/tx_pb2.py#L160)
message, which looks like just what we need. It takes a single field, `validator_address`,
which is a utf-8 string.

The code to send a transaction containing such a message might look something like...

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

## Low Level API - nested messages using protobuf.Any

The above example created and broadcast a simple `MsgWithdrawValidatorCommission` message.  
However sometimes it is necessary to include one message in another. For example what if
we wanted to use the above message, but execute it from a different account using authz?
(ie use an account which holds minimal funds, whose keys need not be treated with the
same level of care as those of the validator itself).

In this case, we'll need to send an authz
[MsgExec](https://github.com/fetchai/cosmpy/blob/4abb976753edcab402fcc23d4dce3ab67b73b608/cosmpy/protos/cosmos/authz/v1beta1/tx_pb2.py#L114)
message, which we found by browsing the
[tx_pb2.py](https://github.com/fetchai/cosmpy/blob/4abb976753edcab402fcc23d4dce3ab67b73b608/cosmpy/protos/cosmos/authz/v1beta1/tx_pb2.py) file in the cosmos/authz area of the cosmpy/protos.
This message consists of two fields. The "grantee" is a simple string address, as above.
But the msgs field needs to support multiple types of message, not just
MsgWithdrawValidatorCommission.
Protobuf is strongly typed, so to facilitate this flexibility, it is necesssary to first pack the
nested message into a protobuf.Any message.

Therefore we arrive at code looking something like...

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

## Low Level API - more protobuf examples

However, before running the above, the necessary authz grant must first be put in place.
For Ledger Nano users (other hardware wallets are available), that might mean an excursion
to the command line, such as...

```bash
fetchd tx authz grant $(fetchd keys show grantee --output json | jq -r .address) generic --msg-type "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward" --from=$(fetchd keys show grantor --output json | jq -r .address) --gas auto --gas-adjustment 1.5 --gas-prices 5000000000atestfet
```

...which, by default, will provide one year's worth of authorization to withdraw delegator
rewards, using accounts already present in the keyring.

But for those with access to their keys in python, and with a bit more handling of protobuf messages...

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
