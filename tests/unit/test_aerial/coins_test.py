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

from cosmpy.aerial.coins import Coin, Coins, OnCollision, parse_coins
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin as CoinProto


@pytest.mark.parametrize(
    "input_coins,expected_result",
    [
        ("", []),
        ("          ", []),
        ("50000atestfet", [CoinProto(amount="50000", denom="atestfet")]),
        (
            "  200foobar   ,      50000atestfet ",
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
                CoinProto(amount="50000", denom="atestfet"),
                CoinProto(
                    amount="500",
                    denom="ibc/0471F1C4E7AFD3F07702BEF6DC365268D64570F7C1FDC98EA6098DD6DE59817B",
                ),
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
        (
            "4afet,5afet",
            None,
            'Attempt to merge a coin with the "afet" denomination which already exists in the receiving coins instance',
        ),
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
            [Coin(2, "acc"), CoinProto(amount="4", denom="bcc")],
            [Coin(2, "acc"), Coin(4, "bcc")],
            None,
        ),
        (
            "4acc,2ccc,5bcc",
            "4acc,5bcc,2ccc",
            None,
        ),
        (
            "4cc",
            None,
            'The "cc" denom does not conform to Cosmos-SDK requirements',
        ),
        (
            "4acc,5ccc,0bcc",
            "4acc,5ccc",
            None,
        ),
        (
            "3ecc,2ccc,0dcc,1bcc,0acc",
            "1bcc,2ccc,3ecc",
            None,
        ),
        (
            "0ecc,0ccc,0dcc,0bcc,0acc",
            "",
            None,
        ),
    ],
)
def test_coins_instantiate(input_coins, expected_coins, validate_error):
    """Test Coins instantiate."""
    if validate_error:
        with pytest.raises(Exception) as exc_info:
            _ = Coins(input_coins)
        assert validate_error in str(exc_info.value)

    if not validate_error:
        instantiated_input_coins = Coins(input_coins)
        assert instantiated_input_coins == Coins(expected_coins)


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res",
    [
        ("4acc,2ccc", "2ccc,5bcc", "4acc,5bcc,4ccc"),
    ],
)
def test_add(coins_a, coins_b, expected_coins_res):
    """Test Coins add."""
    coins_a = Coins(coins_a)
    coins_b = Coins(coins_b)
    coins_res = coins_a + coins_b

    expected_coins_res = Coins(expected_coins_res)

    assert coins_res == expected_coins_res


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res,error",
    [
        ("4acc,2ccc", "2ccc", "4acc", None),
        ("4acc,2ccc,5ddd", "1ddd", "4acc,2ccc,4ddd", None),
        ("4acc,2ccc", "2ccc,4acc", "", None),
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
    coins_b = Coins(coins_b)

    if error:
        with pytest.raises(Exception) as exc_info:
            _ = coins_a - coins_b
            assert error in str(exc_info.value)
    else:
        coins_res = coins_a - coins_b

        expected_coins_res = Coins(expected_coins_res)

        assert coins_res == expected_coins_res


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res,error",
    [
        ("", "1ccc", "1ccc", None),
        (None, "3gcc,1ccc", "1ccc,3gcc", None),
        ("1ccc", "", "1ccc", None),
        ("3gcc,1ccc", None, "1ccc,3gcc", None),
        (
            "4acc,2ccc",
            "2ccc",
            None,
            'Attempt to merge a coin with the "ccc" denomination which already exists in the receiving coins instance',
        ),
        ("4acc,2ccc", "1bcc", "4acc,1bcc,2ccc", None),
        (
            "4acc,2ccc,5ddd",
            "1ccc",
            None,
            'Attempt to merge a coin with the "ccc" denomination which already exists in the receiving coins instance',
        ),
        ("4acc,2ccc,5ddd", "1edd", "4acc,2ccc,5ddd,1edd", None),
    ],
)
def test_merge_coins_fail_on_collision(coins_a, coins_b, expected_coins_res, error):
    """Test Coins merge with fail on collision."""
    coins_a1 = Coins(coins_a)
    coins_a2 = Coins(coins_a)
    coins_a3 = Coins(coins_a)
    coins_a4 = Coins(coins_a)
    coins_a5 = Coins(coins_a)

    if error:
        with pytest.raises(Exception) as exc_info:
            coins_a1.merge_from(coins_b)
        assert error in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            coins_a2.merge_from(coins_b, on_collision=OnCollision.Fail)
        assert error in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            coins_a3 <<= coins_b
        assert error in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            coins_a4 << coins_b
        assert error in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            Coins(coins_b) >> coins_a5
        assert error in str(exc_info.value)
    else:
        expected_coins_res = Coins(expected_coins_res)

        coins_a1.merge_from(coins_b)
        assert coins_a1 == expected_coins_res

        coins_a2.merge_from(coins_b, on_collision=OnCollision.Fail)
        assert coins_a2 == expected_coins_res

        coins_a3 <<= coins_b
        assert coins_a3 == expected_coins_res

        coins_a4_merged = coins_a4 << coins_b
        assert coins_a4_merged == expected_coins_res


@pytest.mark.parametrize(
    "coins_a,coins_b,expected_coins_res,error",
    [
        ("", "1ccc", "1ccc", None),
        (None, "3gcc,1ccc", "1ccc,3gcc", None),
        ("1ccc", "", "1ccc", None),
        ("3gcc,1ccc", None, "1ccc,3gcc", None),
        ("4acc,2ccc", "3gcc,1ccc", "4acc,1ccc,3gcc", None),
        ("4acc,2ccc", "1ccc", "4acc,1ccc", None),
        ("4acc,2ccc,5ddd,7ecc", "1acc,3ccc,6ddd", "1acc,3ccc,6ddd,7ecc", None),
        ("4acc,2ccc,5ddd", "1acc,3ccc,6ddd,7ecc", "1acc,3ccc,6ddd,7ecc", None),
        ("4acc,2ccc,5ddd", "1acc,7ecc", "1acc,2ccc,5ddd,7ecc", None),
    ],
)
def test_merge_coins_override_on_collision(coins_a, coins_b, expected_coins_res, error):
    """Test Coins merge with override on collision."""
    expected_coins_res = Coins(expected_coins_res)

    coins_a1 = Coins(coins_a)

    coins_a1.merge_from(coins_b, on_collision=OnCollision.Override)
    assert coins_a1 == expected_coins_res


@pytest.mark.parametrize(
    "coins_a",
    [
        (None),
        (""),
        ("1ccc"),
        ("4acc,2ccc,5ddd,7ecc"),
    ],
)
def test_clear(coins_a):
    """Test Coins clear."""
    coins = Coins(coins_a)

    x = coins.clear()
    assert len(coins) == 0
    assert x == coins
