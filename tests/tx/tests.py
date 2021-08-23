# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Tests for REST implementation of Tx."""

import os
import unittest
from dataclasses import dataclass
from hashlib import sha256

from google.protobuf.any_pb2 import Any
from grpc import insecure_channel

from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey, PublicKey
from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from cosmpy.protos.cosmos.auth.v1beta1.query_pb2_grpc import (
    QueryStub as AuthQueryClient,
)
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.protos.cosmos.crypto.secp256k1.keys_pb2 import PubKey as ProtoPubKey
from cosmpy.protos.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import (
    BroadcastMode,
    BroadcastTxRequest,
)
from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import (
    AuthInfo,
    Fee,
    ModeInfo,
    SignDoc,
    SignerInfo,
    Tx,
    TxBody,
)
from cosmpy.tx import sign_transaction
from cosmpy.tx.rest_client import TxRestClient


def my_import(name):
    """returns the name of the last module given a dotted path"""
    if name[0] == "/":
        name = name[1:]
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


@dataclass
class TxSerialisedTestData:
    """Data class for transactions"""

    private_key: str
    tx_body: str
    tx: str
    sign_doc_bytes: str
    hash_for_signing: str

    def __post_init__(self):
        if isinstance(self.private_key, str):
            self.private_key = bytes.fromhex(self.private_key)
        if isinstance(self.tx_body, str):
            self.tx_body = bytes.fromhex(self.tx_body)
        if isinstance(self.tx, str):
            self.tx = bytes.fromhex(self.tx)
        if isinstance(self.sign_doc_bytes, str):
            self.sign_doc_bytes = bytes.fromhex(self.sign_doc_bytes)
        if isinstance(self.hash_for_signing, str):
            self.hash_for_signing = bytes.fromhex(self.hash_for_signing)


class TxSign(unittest.TestCase):
    """Test case of Tx module."""

    tx_test_data = TxSerialisedTestData(
        private_key="0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae",
        tx_body="0a8a010a1c2f636f736d6f732e62616e6b2e763162657461312e4d736753656e64126a0a2b7761736d316d72663579796a6e6e6c707930656776706b3270766a646b393636376a326774397877737a63122b7761736d313238723833757663786e7338323533356433646135776d667668633265356d756a796a6d786a1a0e0a0575636f736d12053132333435121d486176652066756e207769746820796f7572207374617220636f696e73",
        tx="0aac010a8a010a1c2f636f736d6f732e62616e6b2e763162657461312e4d736753656e64126a0a2b7761736d316d72663579796a6e6e6c707930656776706b3270766a646b393636376a326774397877737a63122b7761736d313238723833757663786e7338323533356433646135776d667668633265356d756a796a6d786a1a0e0a0575636f736d12053132333435121d486176652066756e207769746820796f7572207374617220636f696e7312670a500a460a1f2f636f736d6f732e63727970746f2e736563703235366b312e5075624b657912230a2102935ee91bcdd32610db433cceec287e852ba21ad7ff368a0d6174ec59dad71c3f12040a020801180112130a0d0a0575636f736d1204323030301080f1041a4064d060aad828a4a31ef779455a27c30349c602aaca22924cbb6ed982a6c19aa7239da91af10936c3e34304771e31b8abb3588bb7dd7526260c31236cf2a6588a",
        sign_doc_bytes="0aac010a8a010a1c2f636f736d6f732e62616e6b2e763162657461312e4d736753656e64126a0a2b7761736d316d72663579796a6e6e6c707930656776706b3270766a646b393636376a326774397877737a63122b7761736d313238723833757663786e7338323533356433646135776d667668633265356d756a796a6d786a1a0e0a0575636f736d12053132333435121d486176652066756e207769746820796f7572207374617220636f696e7312670a500a460a1f2f636f736d6f732e63727970746f2e736563703235366b312e5075624b657912230a2102935ee91bcdd32610db433cceec287e852ba21ad7ff368a0d6174ec59dad71c3f12040a020801180112130a0d0a0575636f736d1204323030301080f1041a0774657374696e67",
        hash_for_signing="c0aeb7763e9a6e0a3371c2f2eb7f1271702f6d58f9af5bb56a5a93a0b2a895f0",
    )

    def test_deserialise_message_from_tx_body(self):
        """Test deserialising message from tx body with positive result."""
        body = TxBody()
        body.ParseFromString(self.tx_test_data.tx_body)
        print("===> body:", body)
        print("===> body.memo:", body.memo)

        for m in body.messages:
            if m.type_url is MsgSend.DESCRIPTOR:
                msg_send = MsgSend()
                m.Unpack(msg_send)
                print("message:", msg_send)
            else:
                print("message:", m)
        tx = Tx()
        tx.ParseFromString(self.tx_test_data.tx)
        print("===> txRaw:", tx)
        print("======> Tx.body: ", tx.body)
        print("======> Tx.auth_info: ", tx.auth_info)
        for sig in tx.signatures:
            print("signature: ", sig)

    def test_sign(self):
        """Test various fields of a serialised Tx remain intact when deserialised then serialised again."""
        tx = Tx()
        tx.ParseFromString(self.tx_test_data.tx)

        sd_reference = SignDoc()
        sd_reference.ParseFromString(self.tx_test_data.sign_doc_bytes)

        print("SignDoc: ", sd_reference)
        print("account number: ", sd_reference.account_number)
        assert sd_reference.SerializeToString() == self.tx_test_data.sign_doc_bytes

        # Constructing our own SignDoc (from original(reference) Tx & SignDoc data)
        sd2 = SignDoc()
        sd2.body_bytes = tx.body.SerializeToString()
        sd2.auth_info_bytes = tx.auth_info.SerializeToString()
        sd2.chain_id = sd_reference.chain_id
        sd2.account_number = sd_reference.account_number

        sd2_data = sd2.SerializeToString()

        assert sd2_data == self.tx_test_data.sign_doc_bytes

        m = sha256()
        m.update(sd2_data)
        hash_for_signing = m.digest()

        assert hash_for_signing == self.tx_test_data.hash_for_signing

        pk = PrivateKey(self.tx_test_data.private_key)

        # Prove that puk key generated from the private key matches the public key provided in the **original/reference** transaction
        reference_pubk = ProtoPubKey()
        tx.auth_info.signer_infos[0].public_key.Unpack(reference_pubk)
        assert pk.public_key_bytes == reference_pubk.key

        pubk = PublicKey(pk.public_key_bytes)

        # Verify signature provided in the **original/reference** transaction
        print("signature: ", tx.signatures[0])
        assert pubk.verify_digest(
            digest=self.tx_test_data.hash_for_signing, signature=tx.signatures[0]
        )

        # Generating deterministic signature:
        deterministic_signature = pk.sign_digest(hash_for_signing, deterministic=True)
        # Quite *unnecessary* verification of the freshly generated signature:
        assert pubk.verify_digest(
            digest=self.tx_test_data.hash_for_signing, signature=deterministic_signature
        )

        # =======================================
        # !!! NOTE !!!: It looks like cosmos-cli generated non-deterministic signatures, since following assert fails
        # assert tx.signatures[0] == deterministic_signature
        # =======================================

    @staticmethod
    @unittest.skipIf(
        "FETCHD_GRPC_URL" not in os.environ, "Just for testing with local fetchd node"
    )
    def test_tx_broadcast():
        """Test broadcasting tx is correct with positive result."""
        from_pk = PrivateKey(
            bytes.fromhex(
                "cfb265b5d54ace71f6adc93a5072da3b8d6bfa8941904b1f6d4197db0c6f677e"
            )
        )
        from_address = Address(from_pk)
        print("validator = ", from_address)

        to_pb = PrivateKey(
            bytes.fromhex(
                "bc689e9f5e3f4e74f3686423fb23aaee25eb96e926bb1d33196c0bf5b482d003"
            )
        )
        to_address = Address(to_pb)

        channel = insecure_channel(os.environ["FETCHD_GRPC_URL"])
        # NOTE(pb): Commented-out code intentionally left in as example:
        # tx_client = TxGrpcClient(channel)
        rest_client = RestClient("http://localhost:1317")
        tx_client = TxRestClient(rest_client)
        auth_query_client = AuthQueryClient(channel)
        account_response = auth_query_client.Account(
            QueryAccountRequest(address=str(from_address))
        )
        account = BaseAccount()
        if account_response.account.Is(BaseAccount.DESCRIPTOR):
            account_response.account.Unpack(account)
        else:
            raise TypeError("Unexpected account type")
        print("account = ", account)

        msg_send = MsgSend()
        msg_send.from_address = str(from_address)
        msg_send.to_address = str(to_address)
        amount = Coin()
        amount.amount = "1"
        amount.denom = "afet"
        msg_send.amount.extend([amount])

        tx_body = TxBody()
        tx_body.memo = "very first tx"
        # NOTE(pb): Commented-out code intentionally left in as example:
        # tx_body.timeout_height = 0xffffffffffffffff
        send_msg_packed = Any()
        send_msg_packed.Pack(msg_send, type_url_prefix="/")
        tx_body.messages.extend([send_msg_packed])

        from_pub_key_pb = ProtoPubKey()
        from_pub_key_pb.key = from_pk.public_key_bytes

        single = ModeInfo.Single()
        single.mode = SignMode.SIGN_MODE_DIRECT
        mode_info = ModeInfo(single=single)

        from_pub_key_packed = Any()
        from_pub_key_packed.Pack(from_pub_key_pb, type_url_prefix="/")
        signer_info = SignerInfo(
            public_key=from_pub_key_packed,
            mode_info=mode_info,
            sequence=account.sequence,
        )
        auth_info = AuthInfo(
            signer_infos=[signer_info],
            fee=Fee(amount=[Coin(amount="0", denom="afet")], gas_limit=200000),
        )

        tx = Tx(body=tx_body, auth_info=auth_info)
        sign_transaction(
            tx,
            signer=from_pk,
            chain_id="testing",
            account_number=account.account_number,
            deterministic=True,
        )
        print("new Tx = ", tx)

        tx_data = tx.SerializeToString()
        broad_tx_req = BroadcastTxRequest(
            tx_bytes=tx_data, mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        broad_tx_resp = tx_client.BroadcastTx(broad_tx_req)

        print("broad_tx_resp = ", broad_tx_resp)
