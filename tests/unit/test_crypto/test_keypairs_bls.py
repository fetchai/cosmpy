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
