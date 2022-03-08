import pytest

from cosmpy.aerial.coins import parse_coins
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


@pytest.mark.parametrize("input_coins,expected_result", [
    ("", []),
    ("          ", []),
    ("50000atestfet", [Coin(amount='50000', denom='atestfet')]),
    ("50000atestfet,     200foobar", [Coin(amount='50000', denom='atestfet'), Coin(amount='200', denom='foobar')]),
])
def test_parsing_coins(input_coins, expected_result):
    assert parse_coins(input_coins) == expected_result
