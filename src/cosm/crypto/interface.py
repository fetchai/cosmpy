from abc import ABC, abstractmethod


class Signer(ABC):
    @abstractmethod
    def sign(self, message: bytes, deterministic=False) -> bytes: ...

    @abstractmethod
    def sign_digest(self, digest: bytes, deterministic=False) -> bytes: ...
