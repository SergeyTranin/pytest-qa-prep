import pytest
from calculator import multiply

# Multiplication tests
@pytest.mark.parametrize("number1, number2, expected_result", [
    (1, 2, 2),
    (-1, 3, -3),
    (10, -4, -40),
    (-100, -200, 20000),
    (777, 678, 526806),
    (999, 0, 0),
    (100000, 100000, 10000000000),
    (1.5, 2, 3.0),
    (-2.5, 4, -10.0),
])
def test_multiply(number1, number2, expected_result):
    assert multiply(number1, number2) == pytest.approx(expected_result)