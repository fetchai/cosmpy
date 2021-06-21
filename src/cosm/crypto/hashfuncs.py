import hashlib


def sha256(contents: bytes) -> bytes:
    h = hashlib.sha256()
    h.update(contents)
    return h.digest()


def ripemd160(contents: bytes) -> bytes:
    if "ripemd160" not in hashlib.algorithms_available:
        raise RuntimeError("ripemd160 hash not supported on your platform")

    h = hashlib.new("ripemd160")
    h.update(contents)
    return h.digest()
