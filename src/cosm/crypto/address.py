from typing import Union, Optional

import bech32
from cosm.crypto.hashfuncs import sha256, ripemd160
from cosm.crypto.keypairs import PublicKey

DEFAULT_PREFIX = "fetch"


def _to_bech32(prefix: str, data: bytes) -> str:
    data_base5 = bech32.convertbits(data, 8, 5, True)
    if data_base5 is None:
        raise RuntimeError("Unable to parse address")
    return bech32.bech32_encode(prefix, data_base5)


class Address:
    def __init__(
        self,
        value: Union[str, bytes, PublicKey, "Address"],
        prefix: Optional[str] = None,
    ):
        if prefix is None:
            prefix = DEFAULT_PREFIX

        if isinstance(value, str):
            _, data_base5 = bech32.bech32_decode(value)
            if data_base5 is None:
                raise RuntimeError("Unable to parse address")

            data_base8 = bech32.convertbits(data_base5, 5, 8, False)
            if data_base8 is None:
                raise RuntimeError("Unable to parse address")

            self._address = bytes(data_base8)
            self._display = value

        elif isinstance(value, bytes):
            if len(value) != 20:
                raise RuntimeError("Incorrect address length")

            self._address = value
            self._display = _to_bech32(prefix, self._address)

        elif isinstance(value, PublicKey):
            self._address = ripemd160(sha256(value.public_key_bytes))
            self._display = _to_bech32(prefix, self._address)

        elif isinstance(value, Address):
            self._address = value._address
            self._display = value._display

    def __str__(self):
        return self._display

    def __bytes__(self):
        return self._address
