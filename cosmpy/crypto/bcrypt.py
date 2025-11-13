# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Utilities for importing bcrypt-armored private keys."""

import base64
import binascii
import hashlib
import re
from typing import Tuple

import bcrypt
from nacl.secret import SecretBox


BEGIN_RE = re.compile(r"^-{5}BEGIN\s+([A-Z0-9]+)\s+PRIVATE KEY-{5}\s*$")
END_RE = re.compile(r"^-{5}END\s+([A-Z0-9]+)\s+PRIVATE KEY-{5}\s*$")


class ArmorError(ValueError):
    """
    Error raised for malformed armor, KDF issues, or decryption failures.

    :param *args: positional arguments forwarded to ValueError.
    :return: ArmorError instance signaling an armor/KDF/decryption error.
    """


# ---- bcrypt's custom base64 alphabet (Radix-64: ./A-Za-z0-9)
_BCRYPT_B64_ALPHABET = (
    b"./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
)


def _bcrypt_base64_encode(raw: bytes) -> bytes:
    """
    Encode bytes using bcrypt's custom Base64 (no padding).

    :param raw: bytes input buffer to encode.
    :return: bytes encoded string (e.g. 16 bytes -> 22 chars).
    """
    out = bytearray()
    i = 0
    raw_len = len(raw)
    while i < raw_len:
        c1 = raw[i]
        i += 1
        out.append(_BCRYPT_B64_ALPHABET[c1 >> 2])
        c1 = (c1 & 0x03) << 4
        if i >= raw_len:
            out.append(_BCRYPT_B64_ALPHABET[c1])
            break
        c2 = raw[i]
        i += 1
        c1 |= c2 >> 4
        out.append(_BCRYPT_B64_ALPHABET[c1])
        c1 = (c2 & 0x0F) << 2
        if i >= raw_len:
            out.append(_BCRYPT_B64_ALPHABET[c1])
            break
        c3 = raw[i]
        i += 1
        c1 |= c3 >> 6
        out.append(_BCRYPT_B64_ALPHABET[c1])
        out.append(_BCRYPT_B64_ALPHABET[c3 & 0x3F])
    return bytes(out)


def _make_bcrypt_salt_from_hex(
    hexsalt: str, cost: int = 12, version: bytes = b"2a"
) -> bytes:
    """
    Compose a bcrypt salt string from a 16-byte hex salt.

    :param hexsalt: str 32-hex-char salt (16 bytes).
    :param cost: int log2 work factor (e.g. 12).
    :param version: bytes bcrypt version tag (e.g. b"2a").

    :raises ArmorError: if salt has icorrect number of bytes

    :return: bytes bcrypt salt of the form b"$<ver>$<cc>$<22chars>".
    """
    salt_bytes = binascii.unhexlify(hexsalt)
    if len(salt_bytes) != 16:
        raise ArmorError(f"bcrypt salt must be 16 bytes, got {len(salt_bytes)}")
    enc22 = _bcrypt_base64_encode(salt_bytes)
    if len(enc22) < 22:
        # bcrypt salts must be exactly 22 chars (truncate if encoder produced 23/24)
        enc22 = enc22[:22]
    cc = f"{int(cost):02d}".encode("ascii")
    return b"$" + version + b"$" + cc + b"$" + enc22


def _parse_armor_bcrypt(armor_str: str) -> Tuple[str, bytes, str]:
    """
    Parse a bcrypt-armored private key block and extract fields.

    :param armor_str: str full ASCII armor including BEGIN/END lines.

    :raises ArmorError: salt, header, or body is missing or malformed

    :return: tuple (algo: str, ciphertext: bytes, salt_hex: str).
    """
    lines = [ln.rstrip("\r\n") for ln in armor_str.splitlines()]
    if not lines or not BEGIN_RE.match(lines[0].strip()):
        raise ArmorError("missing BEGIN header")

    headers, body_lines, in_body = {}, [], False
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        if END_RE.match(line):
            break
        if not in_body:
            if not line:
                in_body = True
            elif ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
            else:
                in_body = True
                if line:
                    body_lines.append(line)
        else:
            if line and not line.startswith("="):  # ignore CRC line
                body_lines.append(line)
        i += 1
    if i >= len(lines) or not END_RE.match(lines[i].strip()):
        raise ArmorError("missing END header")

    if headers.get("kdf", "").lower() != "bcrypt":
        raise ArmorError(f"unrecognized KDF (expected bcrypt): {headers.get('kdf')!r}")

    salt_hex = headers.get("salt", "")
    if not salt_hex:
        raise ArmorError("missing salt header")

    algo = headers.get("type", "") or "secp256k1"

    try:
        ciphertext = base64.b64decode("".join(body_lines), validate=True)
    except binascii.Error as e:
        raise ArmorError(f"invalid base64 body: {e}") from e

    return algo, ciphertext, salt_hex


def _derive_key32_bcrypt(passphrase: str, salt_hex: str, rounds: int = 12) -> bytes:
    """
    Derive a 32-byte key using bcrypt then SHA-256.

    :param passphrase: str passphrase to hash.
    :param salt_hex: str 32-hex-char salt (16 bytes).
    :param rounds: int bcrypt cost (log2 work factor).
    :return: bytes 32-byte derived key (sha256(bcrypt(...))).
    """
    salt_str = _make_bcrypt_salt_from_hex(salt_hex, cost=rounds)  # e.g. b"$2a$12$<22>"
    key_raw = bcrypt.hashpw(passphrase.encode("utf-8"), salt_str)
    return hashlib.sha256(key_raw).digest()


def _secretbox_decrypt_prefixed_nonce(ciphertext: bytes, key32: bytes) -> bytes:
    """
    Decrypt XSalsa20-Poly1305 ciphertext with a prefixed 24-byte nonce.

    :param ciphertext: bytes nonce||ciphertext (nonce is first 24 bytes).
    :param key32: bytes 32-byte SecretBox key.

    :raises ArmorError: if ciphertext or key32 are incorrect

    :return: bytes plaintext on successful authentication/decryption.
    """
    if len(key32) != 32:
        raise ArmorError("key must be 32 bytes")
    if len(ciphertext) <= 24 + SecretBox.MACBYTES:
        raise ArmorError("ciphertext too short")
    nonce, ct = ciphertext[:24], ciphertext[24:]
    return SecretBox(key32).decrypt(ct, nonce)


def import_cosmos_bcrypt_armored_privkey(
    armor_str: str, passphrase: str, rounds: int = 12
):
    """
    Import a Cosmos/Tendermint bcrypt-armored private key.

    :param armor_str: str full ASCII armor including headers and body.
    :param passphrase: str passphrase for bcrypt KDF.
    :param rounds: int bcrypt cost (log2 work factor).

    :raises ArmorError: if passphrase is wrong or keyfile is corrupted

    :return: tuple (privkey32: bytes, algo: str) where privkey32 is 32 bytes.
    """
    algo, ciphertext, salt_hex = _parse_armor_bcrypt(armor_str)
    key32 = _derive_key32_bcrypt(passphrase, salt_hex, rounds=rounds)
    try:
        plaintext = _secretbox_decrypt_prefixed_nonce(ciphertext, key32)
    except Exception as e:
        raise ArmorError(
            "decryption failed (wrong passphrase or corrupted keyfile)"
        ) from e

    return plaintext[-32:], algo
