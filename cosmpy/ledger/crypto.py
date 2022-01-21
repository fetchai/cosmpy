from pathlib import Path
from typing import Optional

from cosmpy.common.loggers import get_logger
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey

_logger = get_logger(__name__)


class CosmosCrypto:
    """
    Class that represents user on a blockchain.
    Hold private key to one user and can sign transactions.
    """

    def __init__(
        self,
        private_key: PrivateKey,
        prefix: Optional[str] = None,
        account_number: Optional[int] = None,
    ):
        """
        Init ldger crypto key.

        :param private_key: Cosmos PrivateKey instance
        :param prefix: optional key prefix str
        :param account_number: optional account number.
        """

        self.private_key = private_key
        self.prefix = prefix
        self.account_number = account_number

    def get_address(self) -> str:
        """
        Get address.

        :return: address as str
        """

        return str(Address(self.private_key, prefix=self.prefix))

    def get_pubkey_as_str(self) -> str:
        """
        Get public key as string.

        :return: public key as str
        """
        return self.private_key.public_key

    def get_pubkey_as_bytes(self) -> bytes:
        """
        Get public key as bytes.

        :return: public key as bytes
        """
        return self.private_key.public_key_bytes

    def save_key_to_file(self, filename: str):
        """
        Save private key to file.

        :param filename: str, path to file to save key
        """
        Path(filename).write_text(self.as_str())

    def as_str(self) -> str:
        """
        Get private key as string.

        :return: str
        """
        return self.private_key.private_key_hex

    def __bytes__(self) -> bytes:
        """
        Get private key as bytes.

        :return: bytes
        """
        return self.private_key.private_key_bytes
