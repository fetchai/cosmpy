from abc import ABC, abstractmethod

from cosmpy.crypto.address import Address
from cosmpy.crypto.interface import Signer
from cosmpy.crypto.keypairs import PrivateKey, PublicKey


class Wallet(ABC):
    @abstractmethod
    def address(self) -> Address:
        pass

    @abstractmethod
    def public_key(self) -> PublicKey:
        pass

    @abstractmethod
    def signer(self) -> Signer:
        pass


class LocalWallet(Wallet):
    @staticmethod
    def generate() -> "LocalWallet":
        return LocalWallet(PrivateKey())

    def __init__(self, private_key: PrivateKey):
        self._private_key = private_key

    def address(self) -> Address:
        return Address(self._private_key)

    def public_key(self) -> PublicKey:
        return self._private_key

    def signer(self) -> PrivateKey:
        return self._private_key
