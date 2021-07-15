import hashlib
from _hashlib import HASH  # type: ignore


def sha256(contents: bytes) -> bytes:
    h: HASH = hashlib.sha256()
    h.update(contents)
    return h.digest()


def ripemd160(contents: bytes) -> bytes:
    if "ripemd160" not in hashlib.algorithms_available:
        raise RuntimeError("ripemd160 hash not supported on your platform")

    h: HASH = hashlib.new("ripemd160")
    h.update(contents)
    return h.digest()
