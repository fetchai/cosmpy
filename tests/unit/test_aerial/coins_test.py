"""Test coins."""

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
import pytest

from cosmpy.aerial.coins import Coin, Coins, is_coins_sorted, parse_coins, sort_coins
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto


@pytest.mark.parametrize(
    "input_coins,expected_result",
    [
        ("", []),
        ("          ", []),
        ("50000atestfet", [CoinProto(amount="50000", denom="atestfet")]),
        (
            "50000atestfet,     200foobar",
            [
                CoinProto(amount="50000", denom="atestfet"),
                CoinProto(amount="200", denom="foobar"),
            ],
        ),
        (
            "500ibc/0471F1C4E7AFD3F07702BEF6DC365268D64570F7C1FDC98EA6098DD6DE59817B",
            [
                CoinProto(
                    amount="500",
                    denom="ibc/0471F1C4E7AFD3F07702BEF6DC365268D64570F7C1FDC98EA6098DD6DE59817B",
                )
            ],
        ),
        (
            "500ibc/0471F1C4E7AFD3F07702BEF6DC365268D64570F7C1FDC98EA6098DD6DE59817B, 50000atestfet",
            [
                CoinProto(
                    amount="500",
                    denom="ibc/0471F1C4E7AFD3F07702BEF6DC365268D64570F7C1FDC98EA6098DD6DE59817B",
                ),
                CoinProto(amount="50000", denom="atestfet"),
            ],
        ),
    ],
)
def test_parsing_coins_string(input_coins, expected_result):
    """Test parsing coins."""
    assert parse_coins(input_coins) == expected_result
    assert Coins(input_coins).to_proto() == expected_result


@pytest.mark.parametrize(
    "input_coins,expected_coins,validate_error",
    [
        ([], [], None),
        ("4afet,5afet", None, 'Multiple occurrences of the "afet" denomination'),
        ("4acc,2bcc,5ccc", [Coin(4, "acc"), Coin(2, "bcc"), Coin(5, "ccc")], None),
        (
            [
                CoinProto(amount="4", denom="acc"),
                CoinProto(amount="2", denom="bcc"),
                CoinProto(amount="5", denom="ccc"),
            ],
            [Coin(4, "acc"), Coin(2, "bcc"), Coin(5, "ccc")],
            None,
        ),
        (CoinProto(amount="4", denom="acc"), [Coin(4, "acc")], None),
        (Coin(4, "acc"), [Coin(4, "acc")], None),
        (
            [Coin(2, "bcc"), CoinProto(amount="4", denom="acc")],
            [Coin(4, "acc"), Coin(2, "bcc")],
            None,
        ),
        (
            "4acc,2ccc,5bcc",
            [Coin(4, "acc"), Coin(2, "ccc"), Coin(5, "bcc")],
            "Coins are not sorted",
        ),
        (
            "4cc",
            None,
            'The "cc" does not conform to Cosmos-SDK requirements',
        ),
    ],
)
def test_coins_validate(input_coins, expected_coins, validate_error):
    """Test Coins validate."""
    if validate_error:
        with pytest.raises(Exception) as exc_info:
            test_coins = Coins(input_coins)
            test_coins.validate()
        assert validate_error in str(exc_info.value)

    if not validate_error:
        test_coins = Coins(input_coins)
        assert test_coins == expected_coins
        test_coins.validate()


@pytest.mark.parametrize(
    "input_coins,expected_sorted_coins",
    [([], []), ("4acc,2ccc,5bcc", "4acc,5bcc,2ccc")],
)
def test_coins_sort(input_coins, expected_sorted_coins):
    """Test Coins sort."""
    sorted_coins = Coins(input_coins)
    sort_coins(sorted_coins)

    input_coins = Coins(input_coins)
    expected_sorted_coins = Coins(expected_sorted_coins)

    if input_coins != sorted_coins:
        assert not is_coins_sorted(input_coins)

    sort_coins(input_coins)

    assert is_coins_sorted(input_coins)
    assert input_coins == expected_sorted_coins


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res",
    [
        ("4acc,2ccc", "2ccc,5bcc", "4acc,5bcc,4ccc"),
    ],
)
def test_add(coins_a, coins_b, expected_coins_res):
    """Test Coins add."""
    coins_a = Coins(coins_a)
    coins_a.canonicalise()
    coins_b = Coins(coins_b)
    coins_b.canonicalise()
    coins_res = coins_a + coins_b

    expected_coins_res = Coins(expected_coins_res)
    expected_coins_res.canonicalise()

    assert coins_res == expected_coins_res


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res,error",
    [
        ("4acc,2ccc", "2ccc", "4acc", None),
        (
            "4acc,2ccc",
            "2ccc,5bcc",
            None,
            "Subtracting 0bcc - 5bcc would result to negative value",
        ),
    ],
)
def test_subtract(coins_a, coins_b, expected_coins_res, error):
    """Test Coins subtract."""
    coins_a = Coins(coins_a)
    coins_a.canonicalise()
    coins_b = Coins(coins_b)
    coins_b.canonicalise()

    if error:
        with pytest.raises(Exception) as exc_info:
            coins_res = coins_a - coins_b
        assert error in str(exc_info.value)
    else:
        coins_res = coins_a - coins_b

        expected_coins_res = Coins(expected_coins_res)
        expected_coins_res.canonicalise()

        assert coins_res == expected_coins_res
