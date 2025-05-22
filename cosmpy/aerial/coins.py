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

"""Parse the coins."""

import re
from typing import List, Union

from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


def parse_coins(value: str) -> List[Coin]:
    """Parse the coins.

    :param value: coins
    :raises RuntimeError: If unable to parse the value
    :return: coins
    """
    coins = []

    parts = re.split(r",\s*", value)
    for part in parts:
        part = part.strip()
        if part == "":
            continue

        match = re.match(r"^(\d+)(.+)$", part)
        if match is None:
            raise RuntimeError(f"Unable to parse value {part}")

        # extract out the groups
        amount, denom = match.groups()
        coins.append(Coin(amount=amount, denom=denom))

    return coins


CoinsParamType = Union[str, Coin, List[Coin]]


def to_coins(amount: CoinsParamType) -> List[Coin]:
    """
    Convert various fee amount formats into a standardized list of Coin objects.

    Accepts a string in standard Cosmos coin notation (e.g., "100uatom,200afet"), or a single Coin,
    or a list of Coins and returns a corresponding list of Coin instances.

    :param amount: A string representing one or more coins, Coin, or a list of Coin objects.
    :return: A list of Coin objects.
    :raises TypeError: If the input is not a supported type.
    """
    if isinstance(amount, Coin):
        coins = [amount]
    elif isinstance(amount, list):
        coins = amount
    elif isinstance(amount, str):
        coins = parse_coins(amount)
    else:
        raise TypeError("`amount` must be either str or Coin or list of Coin type")

    return coins
