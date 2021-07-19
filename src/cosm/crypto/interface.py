from abc import ABC, abstractmethod


class Signer(ABC):
    @abstractmethod
    def sign(self, message: bytes, deterministic=False, canonicalise: bool = True) -> bytes: ...

    @abstractmethod
    def sign_digest(self, digest: bytes, deterministic=False, canonicalise: bool = True) -> bytes: ...
