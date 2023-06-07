import hashlib
import hmac
import re
from typing import Tuple, List, Optional

from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.mnemonic.words import ENGLISH_MNEMONIC_WORDS

SEED_MIN_BYTE_LEN = 16
HMAC_LEN = hashlib.sha512().digest_size
HMAC_HALF_LEN = HMAC_LEN // 2
MNEMONIC_SALT = "mnemonic"
MNEMONIC_ROUNDS = 2048


def split_hmac(data: bytes) -> Tuple[bytes, bytes]:
    assert len(data) == HMAC_LEN
    return data[:HMAC_HALF_LEN], data[HMAC_HALF_LEN:]


def validate_private_key(private_key: bytes) -> bool:
    try:
        PrivateKey(private_key)
        return True
    except:
        return False


def derive_master_key(seed_bytes: bytes) -> Tuple[bytes, bytes]:
    """
    Derive the master key and chain code from the seed bytes.
    """
    if len(seed_bytes) < SEED_MIN_BYTE_LEN:
        raise ValueError(f"Invalid seed length ({len(seed_bytes)})")

    # Compute HMAC, retry if the resulting private key is not valid
    hmac_out = b""
    hmac_data = seed_bytes
    success = False

    while not success:
        hmac_out = hmac.digest(b'Bitcoin seed', hmac_data, "sha512")

        if validate_private_key(hmac_out[:HMAC_HALF_LEN]):
            break

        hmac_data = hmac_out

    return split_hmac(hmac_out)


def parse_derivation_path(path: str) -> List[int]:
    """
    Parse the derivation path in the form of m/44'/118'/0'/0/0 and return a list of indexes.
    """
    match = re.match(r"^m/(\d{1,3}'?)/(\d{1,3}'?)/(\d{1,3}'?)/(\d{1,3}'?)/(\d{1,3}'?)", path)
    if match is None:
        raise RuntimeError('Invalid derivation path')

    indexes: List[int] = []
    for i in range(1, 6):
        if match.group(i).endswith("'"):
            value = int(match.group(i)[:-1]) | (1 << 31)
        else:
            value = int(match.group(i))

        indexes.append(value)

    return indexes


def derive_child_key_from_index(private_key: bytes, chain_code: bytes, index: int) -> Tuple[bytes, bytes]:
    """
    Derive a child key from the specified private key, chain code and index.
    """
    parsed_private_key = PrivateKey(private_key)
    public_key = parsed_private_key.public_key.public_key_bytes

    is_hardened = index & (1 << 31)

    if is_hardened:
        data_bytes = b"\x00" + private_key + index.to_bytes(4, "big")
    else:
        data_bytes = public_key + index.to_bytes(4, "big")

    il_bytes, ir_bytes = split_hmac(hmac.digest(chain_code, data_bytes, "sha512"))

    # Construct new key secret from iL and current private key
    il_int = int.from_bytes(il_bytes, byteorder="big", signed=False)
    private_key_int = int.from_bytes(private_key, byteorder='big', signed=False)

    new_private_key_int = (il_int + private_key_int) % parsed_private_key.curve.order
    new_private_key_bytes = new_private_key_int.to_bytes(32, "big")

    return new_private_key_bytes, ir_bytes


def derive_child_key(master_private_key: bytes, chain_code: bytes, path: str) -> bytes:
    """
    Derive a child key from a master key and a derivation path.
    """
    indexes = parse_derivation_path(path)

    child_private_key = master_private_key
    for index in indexes:
        child_private_key, chain_code = derive_child_key_from_index(child_private_key, chain_code, index)

    return child_private_key


def validate_mnemonic_and_normalise(mnemonic: str) -> str:
    """
    Validate a mnemonic phrase.
    """
    words = mnemonic.split()
    if len(words) not in [12, 15, 18, 21, 24]:
        raise ValueError("Invalid mnemonic length")

    for word in words:
        if word not in ENGLISH_MNEMONIC_WORDS:
            raise ValueError(f"Invalid mnemonic word: {word}")

    return ' '.join(words)


def derive_seed_from_mnemonic(mnemonic: str, passphrase: Optional[str] = None) -> bytes:
    """
    Derive a seed from a mnemonic phrase.
    """

    # ensure that the mnemonic is valid
    mnemonic = validate_mnemonic_and_normalise(mnemonic)

    salt = MNEMONIC_SALT + (passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), salt.encode(), MNEMONIC_ROUNDS)


def derive_child_key_from_mnemonic(mnemonic: str, path: str, passphrase: Optional[str] = None) -> bytes:
    """
    Derive a child key from a mnemonic phrase and a derivation path.
    """

    # compute the seed bytes from the mnemonic
    seed_bytes = derive_seed_from_mnemonic(mnemonic, passphrase=passphrase)

    # derive the master key from the seed bytes
    master_private_key, master_chain_code = derive_master_key(seed_bytes)

    # derive the child key from the master key, given the specified path
    return derive_child_key(master_private_key, master_chain_code, path)
