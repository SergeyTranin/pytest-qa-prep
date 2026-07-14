import pytest
from legacy.calculator import divide

# Division tests
@pytest.mark.parametrize("number1, number2, expected_result", [
    (10, 2, 5),
    (-27, 3, -9),
    (100, -4, -25),
    (-1000, -500, 2),
    (526806, 678, 777),
    (0, 999, 0),
    (1, 3, 0.3333333333),
    (10000000000, 2, 5000000000),
    (5.5, 2, 2.75),
])
def test_divide(number1, number2, expected_result):
    assert divide(number1, number2) == pytest.approx(expected_result)