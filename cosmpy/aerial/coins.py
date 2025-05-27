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
from dataclasses import dataclass
from typing import List, Optional, Union

from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto


denom_regex = re.compile("^[a-zA-Z][a-zA-Z0-9/-]{2,127}$")


@dataclass
class Coin:
    """Coins."""

    amount: int
    denom: str

    def to_proto(self) -> CoinProto:
        """Convert this type to protobuf schema Coin type."""
        return CoinProto(amount=str(self.amount), denom=self.denom)

    def __repr__(self) -> str:
        """Return string representation of coin."""
        return f"{self.amount}{self.denom}"

    def validate(self):
        """Validate this type based on Cosmos-SDK requirements for Coin.

        :raises ValueError: If amount is negative or denom does not conform to cosmos-sdk requirement for denomination.
        """
        if self.amount < 0:
            raise ValueError("Coin amount must be greater than zero")

        if not is_denom_valid(self.denom):
            raise ValueError(
                f'The "{self.denom}" does not conform to Cosmos-SDK requirements'
            )


class Coins(List[Coin]):
    """Coins."""

    def __init__(
        self,
        coins: Optional[
            Union[str, "Coins", List[Coin], List[CoinProto], Coin, CoinProto]
        ] = None,
    ):
        """Convert any coin representation into Coins."""
        if coins is None:
            super().__init__()
            return

        if isinstance(coins, str):
            _coins = Coins._from_string(coins)
        elif isinstance(coins, Coins):
            _coins = coins
        elif isinstance(coins, Coin):
            _coins = [coins]
        elif isinstance(coins, CoinProto):
            _coins = Coins._from_proto([coins])
        elif isinstance(coins, list):
            if len(coins) == 0:
                _coins = []
            elif isinstance(coins[0], Coin):
                _coins = coins
            elif isinstance(coins[0], CoinProto):
                _coins = Coins._from_proto(coins)
            else:
                raise TypeError()
        else:
            raise ValueError(f"Invalid type {type(coins)}")

        super().__init__(_coins)

    def __repr__(self) -> str:
        """Return string representation of Coins."""
        return ",".join([str(c) for c in self[:]])

    def to_proto(self) -> List[CoinProto]:
        """Convert this type to protobuf schema Coins type."""
        return [CoinProto(amount=str(c.amount), denom=c.denom) for c in self]

    def canonicalise(self):
        """Reorganise the value of the instance (list of coins) in to canonical form defined by cosmos-sdk for `Coins`.

        This means alphabetically sorting (ascending) the coins based on denomination.
        The algorithm *fails* with exception *if* each denomination in the list is *not* unique = if some denominations
        are present in the coin list more than once.
        """
        sort_coins(self)
        self.validate()

    def validate(self):
        """Validate whether current value conforms to canonical form for list of coins defined by cosmos-sdk."""
        validate_coins(self)

    @classmethod
    # def _from_proto(cls, proto_coins: Union["CoinsProto", List[CoinProto]]) -> List[Coin]:
    def _from_proto(cls, proto_coins: Union[List[CoinProto]]) -> List[Coin]:
        """Create aerial Coins from List of CoinProto objects."".

        :param proto_coins: input list of CoinsProto
        :return: List of Coin objects
        """
        return [Coin(amount=int(coin.amount), denom=coin.denom) for coin in proto_coins]

    @classmethod
    def _from_string(cls, value: str) -> List[Coin]:
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
            coins.append(Coin(amount=int(amount), denom=denom))

        return coins

    def __add__(self, other):
        """Perform algebraic vector addition of two coin lists."""
        result = Coins()
        for (left, right) in self._math_operation(other, result_inout=result):
            left.amount += right.amount

        return result

    def __sub__(self, other):
        """Perform algebraic vector subtraction of two coin lists, ensuring no coin has negative value."""
        result = Coins()
        for (left, right) in self._math_operation(other, result_inout=result):
            if left.amount < right.amount:
                raise RuntimeError(
                    f"Subtracting {left} - {right} would result to negative value"
                )
            left.amount -= right.amount

        return result

    def __iadd__(self, other):
        """Perform *in-place* algebraic vector subtraction of two coin lists."""
        result = self
        for (left, right) in self._math_operation(other, result_inout=result):
            left.amount += right.amount

        return result

    def __isub__(self, other):
        """Perform *in-place* algebraic vector subtraction of two coin lists, ensuring no coin has negative value."""
        result = self
        for (left, right) in self._math_operation(other, result_inout=result):
            if left.amount < right.amount:
                raise RuntimeError(
                    f"Subtracting {left} - {right} would result to negative value"
                )
            left.amount -= right.amount

        return result

    def _math_operation(self, other: List[Coin], result_inout: "Coins"):
        self.validate()

        if isinstance(other, Coins):
            other.validate()
        else:
            Coins(other).validate()

        res_dict = {c.denom: Coin(amount=c.amount, denom=c.denom) for c in self}
        for c in other:
            left = res_dict.get(c.denom, Coin(amount=0, denom=c.denom))

            yield left, c

            if left.amount == 0:
                if left.denom in res_dict:
                    del res_dict[left.denom]
            elif left.amount > 0:
                res_dict[left.denom] = left
            else:
                raise RuntimeError(f"Operation between yielded negative amount {left}")

        result_inout.clear()
        result_inout.extend(res_dict.values())
        result_inout.canonicalise()


def parse_coins(value: str) -> List[CoinProto]:
    """Parse the coins.

    :param value: coins encoded in cosmos-sdk string format
    :return: List of CoinProto objects
    """
    return Coins(value).to_proto()


CoinsParamType = Union[str, Coins, List[Coin], List[CoinProto], Coin, CoinProto]


def is_denom_valid(denom: str) -> bool:
    """Return true if coin denom name is valid.

    :param denom: string denom
    :return: bool validity
    """
    return denom_regex.match(denom) is not None


def is_coins_sorted(coins: Union[str, Coins, List[Coin], List[CoinProto]]) -> bool:
    """Return true if given coins representation is sorted.

    :param coins: Any type representing coins
    :return: bool is_sorted
    """
    if not coins:
        return True

    if isinstance(coins, str):
        coins = Coins(coins)

    seen = set()

    last_denom = coins[0].denom
    seen.add(last_denom)

    for c in coins[1:]:
        if last_denom >= c.denom:
            return False

        last_denom = c.denom
        seen.add(last_denom)

    return True


def validate_coins(coins: Union[str, Coins, List[Coin], List[CoinProto]]):
    """Return true if given coins representation is valid.

    :param coins: Any type representing coins
    :raises ValueError: If there are multiple coins with the same denom
    :return: bool validity
    """
    if not coins:
        return

    if isinstance(coins, str):
        coins = Coins(coins)

    if len(coins) == 0:
        return

    def _validate_coin(coin: Union[Coin, CoinProto]):
        """Validate coin.

        :param coin: Coin or CoinProto

        """
        if isinstance(coin, CoinProto):
            coin = Coin(int(coin.amount), coin.denom)

        coin.validate()

    _validate_coin(coins[0])

    seen = set()
    last_denom = coins[0].denom
    seen.add(last_denom)

    for c in coins[1:]:
        if c.denom in seen:
            raise ValueError(f'Multiple occurrences of the "{c.denom}" denomination')

        if last_denom >= c.denom:
            raise ValueError(
                "Coins are not sorted as cosmos-sdk expects it (ascending based on denom)"
            )

        _validate_coin(c)

        last_denom = c.denom
        seen.add(c.denom)


# def sort_coins(coins: Union[Coins, CoinsProto, List[Coin], List[CoinProto]]):
def sort_coins(coins: Union[Coins, List[Coin], List[CoinProto]]):
    """Sort and validate coins collection based on Cosmos-SDK definition of Coins validity.

    Coins collection must be sorted ascending alphabetically based on denomination, and each denomination
    in the collection must be unique = be present in the collection just once.

    :param coins: Coins to sort
    """
    coins.sort(key=lambda c: c.denom, reverse=False)
