# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
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

"""Tests for BLS KeyPair module of the Crypto Package."""
from cosmpy.crypto.keypairs_bls import (
    PrivateKey,
    PublicKey,
    aggregate_signatures,
    verify_aggregated_signatures,
)


def test_basic_usecase():
    """Test common BLS keys and signatures use case."""
    msg = b"some"
    pk1 = PrivateKey()
    signature1 = pk1.sign(msg)
    assert pk1.verify(msg, signature1)
    pk2 = PrivateKey()
    signature2 = pk2.sign(msg)
    assert pk2.verify(msg, signature2)

    pk3 = PrivateKey()
    signature3 = pk3.sign(msg)
    assert pk3.verify(msg, signature3)

    assert not pk3.verify(msg, signature2)

    aggregated_signature = aggregate_signatures(signature1, signature2)

    assert verify_aggregated_signatures([pk1, pk2], [msg] * 2, aggregated_signature)

    assert not verify_aggregated_signatures([pk1, pk3], [msg] * 2, aggregated_signature)


def test_private_key():
    """Test BLS private key class."""
    priv_key = PrivateKey()
    assert priv_key.private_key
    assert len(priv_key.private_key_bytes) == 32
    assert len(priv_key.private_key_hex) == 64

    new_priv_key = PrivateKey(priv_key.private_key_bytes)
    assert priv_key.public_key_bytes == new_priv_key.public_key_bytes

    message = b"some"
    assert priv_key.sign(message) != priv_key.sign_digest(message)


def test_public_key():
    """Test BLS public key class."""
    priv_key = PrivateKey()
    pub_key = PublicKey(priv_key.public_key_bytes)
    assert pub_key.public_key
    assert len(pub_key.public_key_bytes) == 48
    assert len(pub_key.public_key_hex) == 96

    message = b"some"
    signature = priv_key.sign(message)
    signature_for_digest = priv_key.sign_digest(message)

    assert pub_key.verify(message, signature)
    assert pub_key.verify_digest(message, signature_for_digest)

    assert not pub_key.verify(message, signature_for_digest)
    assert not pub_key.verify_digest(message, signature)


def test_pub_key_hardcoded_sgianture_check():
    """Check signature of the pub key provided."""
    pub_key = PublicKey(
        b"\x92\x08eo\xb9\x03\xf1\\\x05\xd4\x8fa\xfd}-\x913\\\x1e~\xe6\xbd\xd3Eu\xf43\x05\x88\xfc\x1f\x18\x08\xf8B\x98\xf6-v\xc0\xcbQvpb\xcf\xe0q"
    )
    message = b"random message"
    signature = b"\x87\xcd\xf8z\xfe|P\xe6\x93\x15H\xdd\x9e&\xbf(\xaa\x06\xb7\xce3\xba\x1e \x0e\xea3\x8f3\xdc$.\x04V\xa9,\xd7\xa1\xf5^\x13\x13\xfeNd\xa8\xcb,\x14\xc3p|Zy\xe8\x95\xf5'%Q\x82\xc9,\xe4\x88x\xae\xd3?\xd0\\D]\xcfQ:\xf6\xb9\xdbK\xf5\xbeS\x16\x05\x06\x15\xfff\x1b\x0f\xf4\x1a\xc4\xeb\xf0"

    assert pub_key.verify(message, signature)


def test_aggregated_signature_hardcoded():
    """Check hardcoded aggragated signature."""
    msg = b"some"
    pub_key1 = PublicKey(
        b"\x84}\x9d\xa2\x90\xa78%?\xb9\x1c\x86/:4\xa4b\x12\x95\xff1\xde\xc6L'P\xd9\x8e\xd0\x0b \x7f \xcd\xfc\xeeO'\xc8d\xbd\x06\x9d\xbb\xb2\xcd\x16R"
    )
    pub_key2 = PublicKey(
        b"\xac\xa7\xf3\x02JSsv\xbf*f\xde\x8c\xec\xa1\x83|\x84\xcc\tU2\xfb /\xce\xb8\xd3$hY\r\xbf\x99/\xa1\xccU\x12\x027z\x1a\xa549\x88\\"
    )
    aggregated_signature = b"\x93\xd9\x80l3[\xaa\xb3\xfa|\xf0\x84\x04O\xac\xe7H\xd6\xa7\xbc \t\x8bB\xdfO\x886\xdbW\xda5F \xfb\x91\xd9\x85x \xab\xeb\xb3\xb3\x10\xc0$M\x02\xcf\x06\xb0L|W\xbb\x1a\xed0\xf6\x17[\xd8\x01\xb5\x96\xf3\xe5\xfbC\x17'\xaf\xe5\xa5\x8e\xc1\xbe\xa1) \xac\x8cC\x1f\xbd\xb8\xfb\x9b\x14!g\xbec\r>"

    assert verify_aggregated_signatures(
        [pub_key1, pub_key2], [msg] * 2, aggregated_signature
    )
