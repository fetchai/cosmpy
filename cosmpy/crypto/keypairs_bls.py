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

"""BLS Crypto KeyPairs (Public Key and Private Key) and utility functions."""
import base64
import hashlib
from typing import Callable, List, Optional

from blspy import (  # type: ignore  # pylint: disable=no-name-in-module
    AugSchemeMPL,
    G1Element,
    G2Element,
)
from blspy import (
    PrivateKey as BLSPrivateKey,  # pylint: disable=no-name-in-module; type: ignore
)
from ecdsa.curves import NIST256p
from ecdsa.keys import SigningKey

from cosmpy.crypto.interface import Signer


class PublicKey:
    """BLS public key class."""

    HASH_FUNCTION: Callable = hashlib.sha256

    def __init__(self, public_key: bytes):
        """
        Initialize.

        :param public_key: bytes.
        """
        self._public_key_bytes = public_key
        self._public_key = base64.b64encode(self._public_key_bytes).decode()
        self._verifying_key = G1Element.from_bytes(self._public_key_bytes)

    @property
    def public_key(self) -> str:
        """
        Get public key.

        :return: str public key.
        """
        return self._public_key

    @property
    def public_key_hex(self) -> str:
        """
        Get public key hex.

        :return: str public key hex.
        """
        return self.public_key_bytes.hex()

    @property
    def public_key_bytes(self) -> bytes:
        """
        Get bytes public key.

        :return: bytes public key.
        """
        return self._public_key_bytes

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify message and signature.

        :param message: bytes message content.
        :param signature: bytes signature.
        :return: bool is message and signature valid.
        """
        digest = self.HASH_FUNCTION(message).digest()
        return self.verify_digest(digest, signature)

    def verify_digest(self, digest: bytes, signature: bytes) -> bool:
        """
        Verify digest.

        :param digest: bytes digest.
        :param signature: bytes signature.
        :return: bool is digest valid.
        """
        return AugSchemeMPL.verify(
            self._verifying_key, digest, G2Element.from_bytes(signature)
        )


class PrivateKey(Signer, PublicKey):
    """BLS private key class."""

    HASH_FUNCTION: Callable = hashlib.sha256

    def __init__(self, private_key: Optional[bytes] = None):
        self._private_key_bytes = private_key or self._generate_bytes()
        self._private_key = base64.b64encode(self._private_key_bytes).decode()
        self._signing_key: BLSPrivateKey = AugSchemeMPL.key_gen(self._private_key_bytes)
        PublicKey.__init__(self, public_key=bytes(self._signing_key.get_g1()))

    @property
    def private_key(self) -> str:
        """
        Get private key.

        :return: str private key.
        """
        return self._private_key

    @property
    def private_key_hex(self) -> str:
        """
        Get private key hex.

        :return: str private key hex.
        """
        return self.private_key_bytes.hex()

    @property
    def private_key_bytes(self) -> bytes:
        """
        Get bytes private key.

        :return: bytes private key.
        """
        return self._private_key_bytes

    @staticmethod
    def _generate_bytes() -> bytes:
        """
        Generate random bytes sequence 32 bytes long.

        :return: bytes
        """
        return SigningKey.generate(curve=NIST256p).to_string()

    def sign(
        self, message: bytes, deterministic: bool = True, canonicalise: bool = True
    ) -> bytes:
        """
        Sign message.

        :param message: bytes message content.
        :param deterministic: bool is deterministic.
        :param canonicalise: bool is canonicalise.

        :return: bytes signed message.
        """
        digest = self.HASH_FUNCTION(message).digest()
        return self.sign_digest(digest)

    def sign_digest(
        self, digest: bytes, deterministic=True, canonicalise: bool = True
    ) -> bytes:
        """
        Sign digest.

        :param digest: bytes digest content.
        :param deterministic: bool is deterministic.
        :param canonicalise: bool is canonicalise.

        :return: bytes signed digest.
        """
        return bytes(AugSchemeMPL.sign(self._signing_key, digest))


def aggregate_signatures(*sigs: List[bytes]) -> bytes:
    """
    Combine signatures into one.

    :param *sigs: list of signatures bytes.
    :return: bytes
    """
    return bytes(AugSchemeMPL.aggregate([G2Element.from_bytes(i) for i in sigs]))


def verify_aggregated_signatures(
    pks: List[PublicKey],
    msgs: List[bytes],
    aggregated_signature: bytes,
    hashfunc=hashlib.sha256,
):
    """
    Verify signatures with pub keys and  messages.

    :param pks: list of public keys
    :param msgs: list of messages
    :param aggregated_signature: aggregated signature bytes
    :param hashfunc: hash method from hashlib. default is hashlib.sha256
    :return: bool
    """
    return verify_aggregated_signatures_digests(
        pks, [hashfunc(i).digest() for i in msgs], aggregated_signature
    )


def verify_aggregated_signatures_digests(
    pks: List[PublicKey], digests: List[bytes], aggregated_signature: bytes
):
    """
    Verify signatures with pub keys and  messages.

    :param pks: list of public keys
    :param digests: list of digests calculated
    :param aggregated_signature: aggregated signature bytes
    :return: bool
    """
    return AugSchemeMPL.aggregate_verify(
        [G1Element.from_bytes(pk.public_key_bytes) for pk in pks],
        digests,
        G2Element.from_bytes(aggregated_signature),
    )
