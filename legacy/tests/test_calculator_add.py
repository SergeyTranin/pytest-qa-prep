import pytest
from calculator import add, subtract, multiply, divide

# Addition tests
@pytest.mark.parametrize("number1, number2, expected_result", [
    (1, 2, 3),
    (-1, 3, 2),
    (-10, 4, -6),
    (-100, -200, -300),
    (777, 678, 1455),
    (999, 0, 999),
    (1000000, 2000000, 3000000),
    (1.5, 2.5, 4.0),
    (-1.5, 3.5, 2.0),
])
def test_add(number1, number2, expected_result):
    assert add(number1, number2) == pytest.approx(expected_result)
