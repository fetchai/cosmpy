import base64
import hashlib
from typing import Union, Optional, Callable
import ecdsa
from ecdsa.curves import Curve
from ecdsa.util import sigencode_string_canonize, sigencode_string
from cosm.crypto.interface import Signer


class PublicKey:
    curve: Curve = ecdsa.SECP256k1
    hash_function: Callable = hashlib.sha256

    def __init__(self, public_key: Union[bytes, "PublicKey", ecdsa.VerifyingKey]):
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
        return self._public_key

    @property
    def public_key_hex(self) -> str:
        return self.public_key_bytes.hex()

    @property
    def public_key_bytes(self) -> bytes:
        return self._public_key_bytes

    def verify(self, message: bytes, signature: bytes):
        success: bool = False

        try:
            success = self._verifying_key.verify(signature, message)

        except ecdsa.keys.BadSignatureError:
            pass

        return success

    def verify_digest(self, digest: bytes, signature: bytes):
        success: bool = False

        try:
            success = self._verifying_key.verify_digest(signature, digest)

        except ecdsa.keys.BadSignatureError:
            pass

        return success


class PrivateKey(PublicKey, Signer):
    def __init__(self, private_key: Optional[bytes] = None):
        if private_key is None:
            self._signing_key = ecdsa.SigningKey.generate(
                curve=self.curve, hashfunc=self.hash_function
            )
        elif isinstance(private_key, bytes):
            self._signing_key = ecdsa.SigningKey.from_string(
                private_key, curve=self.curve, hashfunc=self.hash_function
            )
        else:
            raise RuntimeError("Unable to load private key from input")

        # cache the binary representations of the private key
        self._private_key_bytes = self._signing_key.to_string()
        self._private_key = base64.b64encode(self._private_key_bytes).decode()

        # construct the base class
        super().__init__(self._signing_key.get_verifying_key())

    @property
    def private_key(self) -> str:
        return self._private_key

    @property
    def private_key_hex(self) -> str:
        return self.private_key_bytes.hex()

    @property
    def private_key_bytes(self) -> bytes:
        return self._private_key_bytes

    def sign(self, message: bytes, deterministic=True, canonicalise: bool = True) -> bytes:
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = self._signing_key.sign_deterministic if deterministic else self._signing_key.sign

        return sign_fnc(message, sigencode=sigencode)

    def sign_digest(self, digest: bytes, deterministic=True, canonicalise: bool = True) -> bytes:
        sigencode = sigencode_string_canonize if canonicalise else sigencode_string
        sign_fnc = self._signing_key.sign_digest_deterministic if deterministic else self._signing_key.sign_digest

        return sign_fnc(digest, sigencode=sigencode)
