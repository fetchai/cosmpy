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

"""Crypto KeyPairs (Public Key and Private Key)."""

import base64
import hashlib
from typing import BinaryIO, Callable, Optional, Union

import ecdsa
from ecdsa.curves import Curve
from ecdsa.util import sigencode_string, sigencode_string_canonize

from cosmpy.crypto.bcrypt import import_cosmos_bcrypt_armored_privkey
from cosmpy.crypto.interface import Signer


def _base64_decode(value: str) -> bytes:
    try:
        return base64.b64decode(value)
    except Exception as error:
        raise RuntimeError("Unable to parse base64 value") from error


class PublicKey:
    """Public key class."""

    curve: Curve = ecdsa.SECP256k1
    hash_function: Callable = hashlib.sha256

    def __init__(self, public_key: Union[bytes, "PublicKey", ecdsa.VerifyingKey]):
        """Initialize.

        :param public_key: butes, public key or ecdsa verifying key instance
        :raises RuntimeError: Invalid public key
        """
        if isinstance(public_key, bytes):
            self._verifying_key = ecdsa.VerifyingKey.from_string(
                public_key, curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(public_key, PublicKey):
            self._verifying_key = public_key._verifying_key
        elif isinstance(public_key, ecdsa.VerifyingKey):
            self._verifying_key = public_key
        else:
            raise RuntimeError("Invalid public key type")  # noqa

        self._public_key_bytes: bytes = self._verifying_key.to_string("compressed")
        self._public_key: str = base64.b64encode(self._public_key_bytes).decode()

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
        success: bool = False

        try:
            success = self._verifying_key.verify(signature, message)

        except ecdsa.keys.BadSignatureError:
            ...

        return success

    def verify_digest(self, digest: bytes, signature: bytes) -> bool:
        """
        Verify digest.

        :param digest: bytes digest.
        :param signature: bytes signature.
        :return: bool is digest valid.
        """
        success: bool = False

        try:
            success = self._verifying_key.verify_digest(signature, digest)

        except ecdsa.keys.BadSignatureError:  # pragma: no cover
            ...

        return success


class PrivateKey(Signer):
    """Private key class."""

    curve: Curve = ecdsa.SECP256k1
    hash_function: Callable = hashlib.sha256

    def __init__(self, private_key: Optional[Union[bytes, str]] = None):
        """
        Initialize.

        :param private_key: bytes private key (optional, None by default).
        :raises RuntimeError: if unable to load private key from input.
        """
        if private_key is None:
            self._signing_key = ecdsa.SigningKey.generate(
                curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(private_key, bytes):
            self._signing_key = ecdsa.SigningKey.from_string(
                private_key, curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(private_key, str):
            raw_private_key = _base64_decode(private_key)
            self._signing_key = ecdsa.SigningKey.from_string(
                raw_private_key, curve=self.curve, hashfunc=self.hash_function
            )

        else:
            raise RuntimeError("Unable to load private key from input")

        # cache the binary representations of the private key
        self._private_key_bytes = self._signing_key.to_string()
        self._private_key = base64.b64encode(self._private_key_bytes).decode()

    @classmethod
    def from_bcrypt_key(cls, io: BinaryIO, passphrase: str) -> "PrivateKey":
        """
        Load a PrivateKey from a bcrypt-armored key file.

        :param io: BinaryIO file-like object containing the armored key.
        :param passphrase: str passphrase to decrypt the key.
        :return: PrivateKey instance initialized with the decrypted key.
        :raises ValueError: if the key algorithm is not secp256k1.
        """
        # keep your deterministic account name (hash of file contents)
        raw = io.read()

        # decrypt armor (bcrypt + xsalsa20), get raw privkey bytes
        armor_str = raw.decode("utf-8", errors="strict")
        privkey_bytes, algo = import_cosmos_bcrypt_armored_privkey(
            armor_str, passphrase=passphrase, rounds=12
        )

        if algo.lower() != "secp256k1":
            raise ValueError(f"Unsupported key algo '{algo}', expected secp256k1")

        return cls(privkey_bytes)

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

    @property
    def public_key(self) -> PublicKey:
        """
        Get public key.

        :return: public key.
        """
        return PublicKey(self._signing_key.get_verifying_key())

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
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = (
            self._signing_key.sign_deterministic
            if deterministic
            else self._signing_key.sign
        )

        return sign_fnc(message, sigencode=sigencode)

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
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = (
            self._signing_key.sign_digest_deterministic
            if deterministic
            else self._signing_key.sign_digest
        )

        return sign_fnc(digest, sigencode=sigencode)
