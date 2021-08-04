"""Interface of Crypto module."""

from abc import ABC, abstractmethod


class Signer(ABC):
    """Signer abstract class."""

    @abstractmethod
    def sign(
        self, message: bytes, deterministic=False, canonicalise: bool = True
    ) -> bytes:
        """Perform signing."""
        ...

    @abstractmethod
    def sign_digest(
        self, digest: bytes, deterministic=False, canonicalise: bool = True
    ) -> bytes:
        """Perform digest signing."""
        ...
