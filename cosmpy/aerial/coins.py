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
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Optional, Union

from sortedcontainers import SortedDict

from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto


denom_regex = re.compile("^[a-zA-Z][a-zA-Z0-9/-]{2,127}$")


# @dataclass(frozen=True)
@dataclass
class Coin:
    """Coins."""

    amount: int
    denom: str  # Read-only by design (property setter is left intentionally undefined)
    _denom: str = field(init=False, repr=False, compare=False, hash=False)

    def __init__(self, amount: int, denom: str) -> None:
        is_denom_valid(denom, raise_ex=True)
        self.amount = amount
        self._denom = denom

    def __repr__(self) -> str:
        """Return string representation of coin."""
        return f"{self.amount}{self.denom}"

    # NOTE(pb): The denom property setter is *NOT* defined by-design
    @property  # type: ignore
    def denom(self) -> str:
        """Return denom of coin.
        The denom property setter is *NOT* defined *by-design* in order to avoid misalignment/inconsistencies
        later on in the `Coins` collection class.
        If the denom setter was enabled, then it would allow changing denom value externally = from without knowledge
        of the `Coins` collection class, since the `Coin` is reference type. We want to avoid passing the Coin instance
        always by-value (by-copy).

        :return: denomination of the coin instance
        """

        return self._denom

    def to_proto(self) -> CoinProto:
        """Convert this type to protobuf schema Coin type."""
        return CoinProto(amount=str(self.amount), denom=self.denom)

    def is_valid(self, raise_ex: bool = False) -> bool:
        """Validate Coin instance based on Cosmos-SDK requirements.

        :return: True if the Coin instance conforms to cosmos-sdk requirement for Coin, False otherwise.
        """
        return self.is_amount_valid(raise_ex) and self.is_denom_valid(raise_ex)

    def is_amount_valid(self, raise_ex: bool = False) -> bool:
        """Validate amount value based on Cosmos-SDK requirements.

        :param raise_ex: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

        :return: True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than
                 or equal to  zero). False otherwise.

        :exception ValueError: If `raise_ex` is True and amount does not conform to cosmos-sdk requirement.
        """
        if self.amount > 0:
            return True

        if raise_ex:
            raise ValueError("Coin amount must be greater than zero")

        return False

    def is_denom_valid(self, raise_ex: bool = False) -> bool:
        """Validate denom value based on Cosmos-SDK requirements.

        :return: True if denom conforms to cosmos-sdk requirement for denomination, False otherwise.
        """
        return is_denom_valid(self.denom, raise_ex)


class OnCollision(Enum):
    Fail = 0
    Override = 1


class Coins:
    """Coins."""

    def __init__(
        self,
        coins: Optional[
            Union[str, "Coins", List[Coin], List[CoinProto], Coin, CoinProto]
        ] = None,
    ):
        """Instantiate Coins from any of the supported coin(s) representation types."""

        self._coins: SortedDict[str, Coin] = SortedDict()
        self.assign(coins)

    def __repr__(self) -> str:
        """Return cosmos-sdk string representation of Coins.

        :return: cosmos-sdk formatted string representation of Coins.

        Example::
        from cosmpy.aerial.client.coins import Coin, Coins

        coins = Coins([Coin(1,"afet"), Coin(2,"uatom"), Coin(3,"nanomobx")])
        assert str(coins) == "1afet,2uatom,3nanomobx"
        """
        return ",".join([repr(c) for c in self])

    def __iter__(self):
        for c in self._coins.values():
            # yield Coin(c.amount, c.denom)
            yield c

    def __len__(self) -> int:
        return len(self._coins)

    def __getitem__(self, key: str) -> Coin:
        # NOTE(pb): Should we return by-value rather than by-reference in order to prevent potential external
        #           modifications of the Coin.amount value? However, at the cost performance loss - Coin instance
        #           would need to be cloned on multiple places ...
        c = self._coins[key]
        # return Coin(c.amount, c.denom)
        return c

    # NOTE(pb): Intentionally commented-out since its presence in public API could cause potential confusion.
    #           Either the denom value would need to be passed twice (once as key and once in Coin object value, (e.g.
    #           `coins["mydenom] = Coin(1, "mydenom")`), OR we would need to change the type of the input value to
    #           `int` (`__setitem__(self, key: str, value: int):`, for example `coins["mydenom] = 1`). However, that
    #           would make this method *not* symmetrical with the `__getitem__(self, key: str) -> Coin` counterpart,
    #           which returns the `Coin` type, not `int`.
    # def __setitem__(self, key: str, value: Coin):
    #    if value.denom != key:
    #        raise ValueError(f'Mismatch between the "{key}" key denom and coin denom {value.denom}')
    #    self._merge_coin(coin=value)

    def __contains__(self, denom: str) -> bool:
        return denom in self._coins

    def __delitem__(self, denom: str):
        del self._coins[denom]

    def __eq__(self, right) -> bool:
        if not isinstance(right, Coins):
            right = Coins(right)

        return self._coins == right._coins

    def __hash__(self) -> int:
        return hash(self._coins)

    def clear(self):
        self._coins.clear()

    def assign(
        self,
        coins: Optional[
            Union[str, "Coins", List[Coin], List[CoinProto], Coin, CoinProto]
        ] = None,
    ):
        """Assign value of this ('self') instance from any of the supported coin(s) representation types.

        This means that the current value of this ('self') instance will be completely replaced with a new value
        carried in the input `coins` parameter.
        """

        self.clear()

        if coins is None:
            return

        if isinstance(coins, str):
            self._from_string(coins)
        elif isinstance(coins, Coins):
            self._from_coins_list(coins)
        elif isinstance(coins, (Coin, CoinProto)):
            self._from_coins_list([coins])
        elif isinstance(coins, list):
            if len(coins) == 0:
                pass
            elif isinstance(coins[0], (Coin, CoinProto)):
                self._from_coins_list(coins)
            else:
                raise TypeError(f"Invalid type {type(coins)}")
        else:
            raise ValueError(f"Invalid type {type(coins)}")

    def merge_from(
        self,
        coins: Union[str, "Coins", List[Coin], List[CoinProto], Coin, CoinProto],
        on_collision: OnCollision = OnCollision.Fail,
    ) -> "Coins":
        """Merge passed in coins with this ('self') coins instance.

        :param coins: Input coins in any of supported types.
        :param on_collision: If OnCollision.Override then the coin instance in this (self) object will be overridden if it already
                             contains the denomination, if OnCollision.Fail the merge will fail with exception.
        """
        cs = Coins(coins)

        for c in cs:
            self._merge_coin(c, on_collision)

        return self

    def get_by_index(self, index) -> Coin:
        """Return Coin instance at given `index`.

        If the `index` is out of range, raises :exc:`IndexError`.

        Runtime complexity: `O(log(n))`

        This method poses the same risk to validity of the Coins value as the `__getitem__(...)` method,
        since at the moment it returns Coin instance *by-reference* what allows to change the `Coin.amount` value
        from external context and so potentially invalidate the value represented by the `Coins` class/container.

        Example::
        >>> from cosmpy.aerial.coins import Coin, Coins
        >>> cs = Coins("1aaa,2baa,3caa")
        >>> cs.get_by_index(0)
        1aaa
        >>> cs.get_by_index(2)
        3caa
        >>> cs.get_by_index(3)
        Traceback (most recent call last):
          ...
        IndexError: list index out of range

        :param int index: index of item (default -1)
        :return: key and value pair
        :raises IndexError: if `index` out of range
        """
        _, c = self._coins.peekitem(index)
        # return Coin(c.amount, c.denom)
        return c

    def to_proto(self) -> List[CoinProto]:
        """Convert this type to *protobuf schema* Coins type."""
        return [c.to_proto() for c in self]

    # NOTE(pb): This method should not be necessary, since the API of the Coins class should prevent invalid
    #           Coins values.
    #           However, there is a caveat - the `__getitem__(...)` returns Coin instance by-reference, and so
    #           there is potential for the `Coin.amount` value to be modified from external/caller context.
    #           This can be simply prevented (however at cost of performance loss) by either returning the Coin
    #           instance by-value (a clone), or by disabling setter for `Coin.amount` property, as it has
    #           been done for the `Coin.denom` property.
    def validate(self):
        """Validate whether current value conforms to canonical form for list of coins defined by cosmos-sdk.

        Raises ValueError exception *IF* denominations are not unique, or if validation of individual coins raises an
        exception.
        """
        validate_coins(self)

    def _merge_coin(self, coin: Coin, on_collision: OnCollision = OnCollision.Fail):
        """Merge singular aerial Coin in to this object.

        :param coin: input coin to merge
        :param on_collision: If OnCollision.Override then the coin instance in this (self) object will be overridden
                             if it already contains the denomination, if OnCollision.Fail the merge will fail with
                             an exception.
        """

        if on_collision == OnCollision.Override:
            fail_on_collision = False
        elif on_collision == OnCollision.Fail:
            fail_on_collision = True
        else:
            raise ValueError(f"Unknown on_collision value: {on_collision}")

        is_already_present = coin.denom in self

        if coin.amount == 0:
            if not fail_on_collision and is_already_present:
                del self._coins[coin.denom]

            # Skipping if amount is zero
            return

        if fail_on_collision and is_already_present:
            raise ValueError(
                f'Attempt to merge a coin with the "{coin.denom}" denomination which already exists in the receiving coins instance'
            )

        # # NOTE(pb): This should be the logical equivalent of the code above:
        # if coin.denom in self:
        #    if not fail_on_collision:
        #        if coin.amount == 0:
        #            del self._coins[coin.denom]
        #    else:
        #        if coin.amount == 0:
        #            return
        #
        #        raise ValueError(f'Attempt to merge a coin with the "{coin.denom}" denomination which already exists in the receiving coins instance')
        #
        # if coin.amount == 0:
        #    return
        # # NOTE(pb): End of the equivalent code section.

        coin.is_valid(raise_ex=True)
        self._coins[coin.denom] = coin

    def _from_coins_list(self, coins: Iterable[Union[Coin, CoinProto]]):
        """Create aerial Coins from List of CoinProto objects."".

        :param coins: input list of coins
        """
        for c in coins:
            self._merge_coin(Coin(int(c.amount), c.denom))

    def _from_string(self, value: str):
        """Parse the coins.

        :param value: coins
        :raises RuntimeError: If unable to parse the value
        :return: coins
        """
        parts = re.split(r",\s*", value)
        for part in parts:
            part = part.strip()
            if part == "":
                continue

            match = re.match(r"^(\d+)(.+)$", part)
            if match is None:
                raise RuntimeError(f"Unable to parse value {part}")

            amount, denom = match.groups()
            self._merge_coin(Coin(int(amount), denom))

    def __add__(self, other):
        """Perform algebraic vector addition of two coin lists."""
        result = Coins(self)
        for (left, right) in self._math_operation(other, result_inout=result):
            left.amount += right.amount

        return result

    def __sub__(self, other):
        """Perform algebraic vector subtraction of two coin lists, ensuring no coin has negative value."""
        result = Coins(self)
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

    @staticmethod
    def _math_operation(
        other: Union[str, "Coins", Iterable[Coin], Iterable[CoinProto], Coin, CoinProto],
        result_inout: "Coins",
    ):
        res = result_inout

        if not isinstance(other, Coins):
            other = Coins(other)

        for c in other:
            left = res._coins.get(c.denom, Coin(0, c.denom))

            yield left, c

            # if left.amount == 0:
            #    if left.denom in res:
            #        del res[left.denom]
            # elif left.amount > 0:
            #    # res._merge_coin(left, on_collision=OnCollision.Override)
            #    res._coins[left.denom] = left
            # else:
            #    raise RuntimeError(f"Operation yielded negative amount {left}")
            res._merge_coin(left, on_collision=OnCollision.Override)


def parse_coins(value: str) -> List[CoinProto]:
    """Parse the coins.

    :param value: coins encoded in cosmos-sdk string format
    :return: List of CoinProto objects
    """
    return Coins(value).to_proto()


CoinsParamType = Union[str, Coins, Iterable[Coin], Iterable[CoinProto], Coin, CoinProto]


def is_denom_valid(denom: str, raise_ex: bool = False) -> bool:
    """Check if denom value conforms to Cosmos-SDK requirements.

    :param raise_ex: If True raises exception in case when amount does not conform to cosmos-sdk requirement.

    :return: True if the amount conforms to cosmos-sdk requirement for Coin amount (when it is greater than zero),
             False otherwise.

    :exception ValueError: If `raise_ex` is True and amount does not conform to cosmos-sdk requirement.
    """
    if denom_regex.match(denom) is not None:
        return True

    if raise_ex:
        raise ValueError(
            f'The "{denom}" denom does not conform to Cosmos-SDK requirements'
        )

    return False


def is_coins_sorted(coins: Union[str, Coins, Iterable[Coin], Iterable[CoinProto]]) -> bool:
    """Return true if given coins representation is sorted in ascending order of denom.

    :param coins: Any type representing coins
    :return: bool is_sorted
    """
    if coins is None:
        return False

    if not coins:
        return True

    if isinstance(coins, str):
        coins = Coins(coins)

    itr = iter(coins)
    coin = next(itr, None)

    if coin is None:
        return True

    last_denom = coin.denom
    coin = next(itr, None)

    while coin is not None:
        if last_denom >= coin.denom:
            return False

        last_denom = coin.denom
        coin = next(itr, None)

    return True


def validate_coins(coins: Union[str, Coins, Iterable[Coin], Iterable[CoinProto]]):
    """Return true if given coins representation is valid.

    :param coins: Any type representing coins
    :raises ValueError: If there are multiple coins with the same denom
    :return: bool validity
    """
    if not coins:
        return

    if isinstance(coins, Coins):
        # Only thing which can be possibly wrong at this point is amount value:
        for coin in coins:
            coin.is_amount_valid(raise_ex=True)
    else:
        # Conversion to Coins will verify everything, no need to do anything else:
        _ = Coins(coins)
