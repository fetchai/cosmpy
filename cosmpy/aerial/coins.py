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
        if not self.is_amount_valid():
            raise ValueError("Coin amount must be greater than zero")

        if not self.is_denom_valid():
            raise ValueError(
                f'The "{self.denom}" denom does not conform to Cosmos-SDK requirements'
            )

    def is_valid(self) -> bool:
        """Validate Coin instance based on Cosmos-SDK requirements.

        :return: True if the Coin instance conforms to cosmos-sdk requirement for Coin, False otherwise.
        """
        return self.is_amount_valid() and self.is_denom_valid()

    def is_amount_valid(self) -> bool:
        """Validate amount value based on Cosmos-SDK requirements.

        :return: True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than zero),
                 False otherwise.
        """
        return self.amount > 0

    def is_denom_valid(self) -> bool:
        """Validate denom value based on Cosmos-SDK requirements.

        :return: True if denom conforms to cosmos-sdk requirement for denomination, False otherwise.
        """
        return is_denom_valid(self.denom)


class Coins(List[Coin]):
    """Coins.

    It is required to call the 'canonicalise()' method in order to ensure that the Coins instance conforms to
    Cosmos-SDK requirements for Coins type!
    This is because one way or another, due to the nature of the base List type, it is possible to create such an
    instance of Coins which does not conform to Cosmos-SDK requirements.
    """

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
            _coins = Coins._from_coins_list(coins)
        elif isinstance(coins, Coin):
            _coins = [coins]
        elif isinstance(coins, CoinProto):
            _coins = Coins._from_coins_list([coins])
        elif isinstance(coins, list):
            if len(coins) == 0:
                _coins = []
            elif isinstance(coins[0], (Coin, CoinProto)):
                _coins = Coins._from_coins_list(coins)
            else:
                raise TypeError(f"Invalid type {type(coins)}")
        else:
            raise ValueError(f"Invalid type {type(coins)}")

        super().__init__(_coins)

    def __repr__(self) -> str:
        """Return cosmos-sdk string representation of Coins.

        :return: cosmos-sdk formatted string representation of Coins.

        Example::
        from cosmpy.aerial.client.coins import Coin, Coins

        coins = Coins([Coin(1,"afet"), Coin(2,"uatom"), Coin(3,"nanomobx")])
        assert str(coins) == "1afet,2uatom,3nanomobx"
        """
        return ",".join([str(c) for c in self[:]])

    def to_proto(self) -> List[CoinProto]:
        """Convert this type to *protobuf schema* Coins type."""
        coins = Coins(self).canonicalise()
        return [CoinProto(amount=str(c.amount), denom=c.denom) for c in coins]

    def canonicalise(self) -> "Coins":
        """Reorganise the value of the 'self' instance in to canonical form defined by cosmos-sdk for `Coins`.

        This means dropping all coins with zero value, and alphabetically sorting (ascending) the coins based
        on denomination.
        The algorithm *fails* with exception *if* any of the denominations in the list is *not* unique = if some of the
        denominations are present in the coin list more than once, or if validation of any individual coin will fail.
        :returns: The 'self' instance.
        """
        coins = [c for c in self if c.amount > 0]

        self.clear()
        self.extend(coins)

        sort_coins(self)
        self.validate()

        return self

    def validate(self):
        """Validate whether current value conforms to canonical form for list of coins defined by cosmos-sdk.

        Raises ValueError exception *IF* denominations are not unique, or if validation of individual coins raises an
        exception.
        """
        validate_coins(self)

    @classmethod
    def _from_coins_list(cls, coins: List[Union[Coin, CoinProto]]) -> List[Coin]:
        """Create aerial Coins from List of CoinProto objects."".

        :param coins: input list of CoinsProto
        :return: List of Coin objects
        """
        return [Coin(amount=int(coin.amount), denom=coin.denom) for coin in coins]

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
                raise RuntimeError(f"Operation yielded negative amount {left}")

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
    """Return true if given coins representation is sorted in ascending order of denom.

    :param coins: Any type representing coins
    :return: bool is_sorted
    """
    if not coins:
        return True

    if isinstance(coins, str):
        coins = Coins(coins)

    last_denom = coins[0].denom

    for c in coins[1:]:
        if last_denom >= c.denom:
            return False

        last_denom = c.denom

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
    """Sort the collection of coins based on Cosmos-SDK definition of Coins validity.

    Coins collection is sorted ascending alphabetically based on denomination.

    NOTE: The resulting sorted collection of coins is *NOT* validated by calling the 'Coins.validate()'.

    :param coins: Coins to sort
    """
    coins.sort(key=lambda c: c.denom, reverse=False)
