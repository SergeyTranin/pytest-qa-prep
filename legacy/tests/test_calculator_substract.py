import pytest
from calculator import subtract

# Subtraction tests
@pytest.mark.parametrize("number1, number2, expected_result", [
    (1, 2, -1),
    (-1, 3, -4),
    (-10, 4, -14),
    (-100, -200, 100),
    (777, 678, 99),
    (999, 0, 999),
    (10000000, 5000000, 5000000),
    (5.5, 2.2, 3.3),
    (-3.5, -1.5, -2.0),
])
def test_subtract(number1, number2, expected_result):
    assert subtract(number1, number2) == pytest.approx(expected_result)