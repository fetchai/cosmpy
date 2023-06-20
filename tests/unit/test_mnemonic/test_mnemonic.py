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

"""Tests for mnemonic."""
import random
import string
import unittest

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

from cosmpy.mnemonic import derive_child_key_from_mnemonic, generate_mnemonic


COSMOS_HD_PATH = "m/44'/118'/0'/0/0"


def generate_random_string(length: int) -> str:
    """Generate random string.

    :param length: length of string
    :return: random string
    """
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(letters) for _ in range(length))


@staticmethod
def from_biputils_mnemonic(mnemonic: str, passphrase: str) -> bytes:
    """Generate local wallet from mnemonic.

    :param mnemonic: mnemonic
    :param passphrase: passphrase
    :return: private key
    """
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
    return bip44_def_ctx.PrivateKey().Raw().ToBytes()


class MintRestClientTestCase(unittest.TestCase):
    """Test case of Mnemonic module."""

    @staticmethod
    def test_AnnualProvisionsBase64():
        """Tests for mnemonic."""
        for _ in 0, 10000:
            mnemonic = generate_mnemonic()
            passphrase = generate_random_string(10)

            key = derive_child_key_from_mnemonic(mnemonic, passphrase, COSMOS_HD_PATH)
            biputils_key_bytes = from_biputils_mnemonic(mnemonic, passphrase)
            assert biputils_key_bytes == key
