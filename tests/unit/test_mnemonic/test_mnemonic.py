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
import unittest

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from cosmpy.mnemonic import generate_mnemonic, derive_child_key_from_mnemonic

COSMOS_HD_PATH = "m/44'/118'/0'/0/0"


@staticmethod
def from_biputils_mnemonic(mnemonic: str) -> bytes:
    """Generate local wallet from mnemonic.

    :param mnemonic: mnemonic
    :return: local wallet
    """
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_def_ctx = Bip44.FromSeed(
        seed_bytes, Bip44Coins.COSMOS
    ).DeriveDefaultPath()
    return bip44_def_ctx.PrivateKey().Raw().ToBytes()


class MintRestClientTestCase(unittest.TestCase):
    """Test case of Mnemonic module."""

    @staticmethod
    def test_AnnualProvisionsBase64():
        """Tests for mnemonic."""

        for _ in 0, 1000000:
            mnemonic = generate_mnemonic()
            passphrase = ""  # Optional passphrase
            key = derive_child_key_from_mnemonic(mnemonic, COSMOS_HD_PATH, passphrase)

            biputils_key_bytes = from_biputils_mnemonic(mnemonic)

            assert biputils_key_bytes == key
