"""Example of aerial deploy contract."""
import base64
import json
from json import JSONDecodeError
from typing import Tuple, Optional

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt

from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


class DataEncrypt:
    """Class to encrypt/decrypt data strings with password provided."""

    @classmethod
    def _aes_encrypt(
        cls, password: str, data: bytes
    ) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Encryption schema for private keys

        :param password: plaintext password to use for encryption
        :param data: plaintext data to encrypt

        :return: encrypted data, nonce, tag, salt
        """
        key, salt = cls._password_to_key_and_salt(password)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)  # type:ignore

        return ciphertext, cipher.nonce, tag, salt  # type:ignore

    @staticmethod
    def _password_to_key_and_salt(
        password: str, salt: Optional[bytes] = None
    ) -> Tuple[bytes, bytes]:
        salt = salt or get_random_bytes(16)
        key = scrypt(password, salt, 16, N=2**14, r=8, p=1)  # type: ignore
        return key, salt  # type: ignore

    @classmethod
    def _aes_decrypt(
        cls, password: str, encrypted_data: bytes, nonce: bytes, tag: bytes, salt: bytes
    ) -> bytes:
        """
        Decryption schema for private keys.

        :param password: plaintext password used for encryption
        :param encrypted_data: data to decrypt
        :param nonce:  bytes
        :param tag:  bytes
        :param salt: bytes
        :return: decrypted data as plaintext
        """
        # Hash password
        key, _ = cls._password_to_key_and_salt(password, salt)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            decrypted_data = cipher.decrypt_and_verify(  # type:ignore
                encrypted_data, tag
            )
        except ValueError as e:
            if e.args[0] == "MAC check failed":
                raise ValueError("Decrypt error! Bad password?") from e
            raise  # pragma: nocover
        return decrypted_data

    @classmethod
    def encrypt(cls, data: bytes, password: str) -> bytes:
        """Encrypt data with password."""
        if not isinstance(data, bytes):  # pragma: nocover
            raise ValueError(f"data has to be bytes! not {type(data)}")

        encrypted_data, nonce, tag, salt = cls._aes_encrypt(password, data)

        json_data = {
            "encrypted_data": cls.bytes_encode(encrypted_data),
            "nonce": cls.bytes_encode(nonce),
            "tag": cls.bytes_encode(tag),
            "salt": cls.bytes_encode(salt),
        }
        return json.dumps(json_data).encode()

    @staticmethod
    def bytes_encode(data: bytes) -> str:
        """Encode bytes to ascii friendly string."""
        return base64.b64encode(data).decode()

    @staticmethod
    def bytes_decode(data: str) -> bytes:
        """Decode ascii friendly string to bytes."""
        return base64.b64decode(data)

    @classmethod
    def decrypt(cls, encrypted_data: bytes, password: str) -> bytes:
        """Decrypt data with password provided."""
        if not isinstance(encrypted_data, bytes):  # pragma: nocover
            raise ValueError(
                f"encrypted_data has to be str! not {type(encrypted_data)}"
            )

        try:
            json_data = json.loads(encrypted_data)
            decrypted_data = cls._aes_decrypt(
                password,
                encrypted_data=cls.bytes_decode(json_data["encrypted_data"]),
                nonce=cls.bytes_decode(json_data["nonce"]),
                tag=cls.bytes_decode(json_data["tag"]),
                salt=cls.bytes_decode(json_data["salt"]),
            )
            return decrypted_data
        except (KeyError, JSONDecodeError) as e:
            raise ValueError(f"Bad encrypted key format!: {str(e)}") from e


def encrypt_wallet(wallet: LocalWallet, password: str) -> bytes:
    return DataEncrypt.encrypt(wallet.signer().private_key_bytes, password)


def decrypt_wallet(encrypted_key: bytes, password: str) -> LocalWallet:
    decrypted_key = DataEncrypt.decrypt(encrypted_key, password)
    return LocalWallet(PrivateKey(decrypted_key))


def main():
    wallet = LocalWallet.generate()

    password = "somepassword"
    encrypted_data = encrypt_wallet(wallet, password)

    print(encrypted_data)

    decrypted_wallet = decrypt_wallet(encrypted_data, password)
    assert wallet.address() == decrypted_wallet.address()


if __name__ == "__main__":
    main()
