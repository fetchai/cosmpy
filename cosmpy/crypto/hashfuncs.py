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

"""Hash functions of Crypto package."""

import hashlib

from _hashlib import HASH  # type: ignore  # pylint: disable=no-name-in-module

# Detect if ripemd160 can actually be used in the system. Querying `hashlib.algorithms_available`
# does not mean much and will fail on 22.04 LTS
try:
    hashlib.new("ripemd160")
    _ripemd160_present = True
except ValueError:
    _ripemd160_present = False


def sha256(contents: bytes) -> bytes:
    """
    Get sha256 hash.

    :param contents: bytes contents.

    :return: bytes sha256 hash.
    """
    h: HASH = hashlib.sha256()
    h.update(contents)
    return h.digest()


def _ripemd160_stdlib(contents: bytes) -> bytes:
    h: HASH = hashlib.new("ripemd160")
    h.update(contents)
    return h.digest()


def _ripemd160_mbedtls(contents: bytes) -> bytes:
    from mbedtls import hashlib as alt_hashlib

    h: HASH = alt_hashlib.new("ripemd160")
    h.update(contents)
    return h.digest()


def ripemd160(contents: bytes) -> bytes:
    """
    Get ripemd160 hash.

    :param contents: bytes contents.

    :return: bytes ripemd160 hash.
    """

    # Check if we need to use the fallback hashlib
    if not _ripemd160_present:
        return _ripemd160_mbedtls(contents)

    # Prefer the stdlib implementation
    return _ripemd160_stdlib(contents)
