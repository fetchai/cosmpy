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
from typing import List, Dict, Union, Optional

from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto
import re

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
        return f'{self.amount}{self.denom}'

    def validate(self):
        """Validate this type based on Cosmos-SDK requirements for Coin."""
        if self.amount < 0:
            raise ValueError(f'Coin amount must be greater than zero')

        if not is_denom_valid(self.denom):
            raise ValueError(f'The "{self.denom}" does not conform to Cosmos-SDK requirements')


class Coins(List[Coin]):
    """Coins."""

    #def __init__(self, coins: Optional[Union[str, "Coins", "CoinsProto", List[Coin], List[CoinProto], Coin, CoinProto]] = None) :
    def __init__(self, coins: Optional[Union[str, "Coins", List[Coin], List[CoinProto], Coin, CoinProto]] = None) :
        if coins is None:
            _coins = coins
        if isinstance(coins, str):
            _coins = Coins._from_string(coins)
        elif isinstance(coins, Coins):
            _coins = coins
        #elif isinstance(coins, CoinsProto):
        #    _coins = Coins._from_proto(coins)
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
            raise ValueError(f'Invalid type {type(coins)}')

        super().__init__(_coins)

    def __repr__(self) -> str:
        return ",".join([str(c) for c in self[:]])

    def to_proto(self) -> List[CoinProto]:
        """Convert this type to protobuf schema Coins type."""
        return [CoinProto(amount=str(c.amount), denom=c.denom) for c in self]

    def sort_coins(self):
        sort_coins(self)

    def validate(self):
        validate_coins(self)

    @classmethod
    #def _from_proto(cls, proto_coins: Union["CoinsProto", List[CoinProto]]) -> List[Coin]:
    def _from_proto(cls, proto_coins: Union[List[CoinProto]]) -> List[Coin]:
        """Create aerial Coins from List of CoinProto objects."".

        :param proto_coins: input list of CoinsProto
        :raises RuntimeError: If unable to parse the value
        :return: List of Coin objects
        """
        #if isinstance(proto_coins, CoinsProto):
        #    proto_coins: List[CoinProto] = proto_coins

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

    def __add__(self, other: List[Coin]) -> List[Coin]:
        result = Coins()
        for (left, right) in self._math_operation(other, result_inout=result):
            left.amount += right.amount

        return result

    def __sub__(self, other: List[Coin]) -> List[Coin]:
        result = Coins()
        for (left, right) in self._math_operation(other, result_inout=result):
            if left.amount < right.amount:
                raise RuntimeError(f"Subtracting {left} - {right} would result to negative value")
            left.amount -= right.amount

        return result

    def __iadd__(self, other: List[Coin]) -> List[Coin]:
        result = self
        for (left, right) in self._math_operation(other, result_inout=result):
            left.amount += right.amount

        return result

    def __isub__(self, other: List[Coin]) -> List[Coin]:
        result = self
        for (left, right) in self._math_operation(other, result_inout=result):
            if left.amount < right.amount:
                raise RuntimeError(f"Subtracting {left} - {right} would result to negative value")
            left.amount -= right.amount

        return result

    def _math_operation(self, other: List[Coin], result_inout: "Coins") -> (Coin, Coin):
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


            #if c.denom in res_dict:
            #    yield res_dict[c.denom], c
            #    #if res_dict[c.denom] == 0
            #else:
            #    # Cloning intentionally to avoid potential unexpected values changes of Coin objects leaking in
            #    # to the this(self) through
            #    # values when
            #    # they will be changed in the externally owned `other` object:
            #    res_dict[c.denom] = Coin(c.amount, c.denom)

        result_inout.clear()
        result_inout.extend([c for c in res_dict.values()])
        result_inout.sort_coins()


#class CoinsProto(List[CoinProto]):
#    """List of protobuf Coin objects."""
#
#    def __init__(self, coins: Optional[Union[str, "CoinsProto", List[CoinProto], CoinProto]] = None) :
#        if coins is None:
#            _coins = coins
#        if isinstance(coins, str):
#            _coins = CoinsProto._from_string(coins)
#        elif isinstance(coins, CoinsProto):
#            _coins = coins
#        elif isinstance(coins, CoinProto):
#            _coins = [coins]
#        elif isinstance(coins, list):
#            if len(coins) == 0:
#                _coins = []
#            elif isinstance(coins[0], CoinProto):
#                _coins = coins
#            else:
#                raise ValueError(f'Invalid type {type(coins)}')
#        else:
#            raise ValueError(f'Invalid type {type(coins)}')
#
#        super().__init__(_coins)
#
#    def __repr__(self) -> str:
#        return ",".join([f'{c.amount}{c.denom}' for c in self[:]])
#
#    @classmethod
#    def _from_string(cls, value: str) -> List[CoinProto]:
#        """Parse the string repr. of coins to protobuf Coins.
#
#        :param value: coins
#        :raises RuntimeError: If unable to parse the value
#        :return: coins
#        """
#        coins = []
#
#        parts = re.split(r",\s*", value)
#        for part in parts:
#            part = part.strip()
#            if part == "":
#                continue
#
#            match = re.match(r"^(\d+)(.+)$", part)
#            if match is None:
#                raise RuntimeError(f"Unable to parse value {part}")
#
#            # extract out the groups
#            amount, denom = match.groups()
#            coins.append(CoinProto(amount=amount, denom=denom))
#
#        return coins
#
#    def sort_coins(self):
#        """Cosmos-SDK Coins sort"""
#        sort_coins(self)
#
#    def validate(self):
#        validate_coins(self)


def parse_coins(value: str) -> List[CoinProto]:
    """Parse the coins.

    :param value: coins encoded in cosmos-sdk string format
    :raises RuntimeError: If unable to parse the value
    :return: List of CoinProto objects
    """
    return Coins(value).to_proto()


CoinsParamType = Union[str, Coin, List[Coin]]


#def to_coins(amount: CoinsParamType) -> List[Coin]:
#    """
#    Convert various fee amount formats into a standardized list of Coin objects.
#
#    Accepts a string in standard Cosmos coin notation (e.g., "100uatom,200afet"), or a single Coin,
#    or a list of Coins and returns a corresponding list of Coin instances.
#
#    :param amount: A string representing one or more coins, Coin, or a list of Coin objects.
#    :return: A list of Coin objects.
#    :raises TypeError: If the input is not a supported type.
#    """
#    if isinstance(amount, Coin):
#        coins = [amount]
#    elif isinstance(amount, list):
#        coins = amount
#    elif isinstance(amount, str):
#        coins = parse_coins(amount)
#    else:
#        raise TypeError("`amount` must be either str or Coin or list of Coin type")
#
#    return coins


def is_denom_valid(denom: str) -> bool:
    return denom_regex.match(denom) is not None


#def is_coins_sorted(coins: Union[Coins, CoinsProto, List[Coin], List[CoinProto]]) -> bool:
def is_coins_sorted(coins: Union[str, Coins, List[Coin], List[CoinProto]]) -> bool:
    if not coins:
        return True

    if isinstance(coins, str):
        coins=Coins(coins)

    seen = set()

    last_denom = coins[0].denom
    seen.add(last_denom)

    for c in coins[1:]:
        if last_denom >= c.denom:
            return False

    return True

#def validate_coins(coins: Union[str, Coins, CoinsProto, List[Coin], List[CoinProto]]):
def validate_coins(coins: Union[str, Coins, List[Coin], List[CoinProto]]):
    if not coins:
        return

    if isinstance(coins, str):
        coins = Coins(coins)

    if len(coins) == 0:
        return

    seen = set()

    last_denom = coins[0].denom
    seen.add(last_denom)

    for c in coins[1:]:
        if c.denom not in seen:
            raise ValueError(f'Multiple occurrences of the "{c.denom}" denomination')

        if last_denom >= c.denom:
            raise ValueError(f'Coins are not sorted as cosmos-sdk expects it (ascending based on denom)')

        if isinstance(c, CoinProto):
            c = Coin(int(c.amount), c.denom)

        c.validate()

        last_denom = c.denom
        seen.add(c.denom)


#def sort_coins(coins: Union[Coins, CoinsProto, List[Coin], List[CoinProto]]):
def sort_coins(coins: Union[Coins, List[Coin], List[CoinProto]]):
    """Sort and validate coins collection based on Cosmos-SDK definition of Coins validity.

    Coins collection must be sorted descending alphabetically based on denomination, and each denomination
    in the collection must be unique = be present in the collection just once.

    :param coins: Coins to sort
    """
    coins.sort(key=lambda c: c.denom, reverse=False)
    validate_coins(coins)
