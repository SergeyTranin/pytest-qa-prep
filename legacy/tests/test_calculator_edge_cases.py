import pytest
from legacy.calculator import add, subtract, multiply, divide

# Division by zero tests
@pytest.mark.parametrize(
    "a",
    [
        1,
        0,
        -5,
        1000000,
    ],
)
def test_divide_by_zero(a):
    with pytest.raises(ZeroDivisionError):
        divide(a, 0)

# Invalid input type tests
@pytest.mark.parametrize(
    "a, b",
    [
        ("1", 2),
        (1, "2"),
        (None, 5),
        (5, None),
        ([], 2),
        (2, {}),
    ],
)
def test_invalid_input_types(a, b):
    with pytest.raises((TypeError, ValueError)):
        add(a, b)

@pytest.mark.parametrize(
    "a, b",
    [
        ("5", 2),
        (5, "2"),
        (None, 2),
        (2, None),
    ],
)
def test_invalid_subtraction_types(a, b):
    with pytest.raises((TypeError, ValueError)):
        subtract(a, b)

@pytest.mark.parametrize(
    "a, b",
    [
        ("5", 2),
        (5, "2"),
        (None, 2),
        (2, None),
    ],
)
def test_invalid_multiplication_types(a, b):
    with pytest.raises((TypeError, ValueError)):
        multiply(a, b)

@pytest.mark.parametrize(
    "a, b",
    [
        ("5", 2),
        (5, "2"),
        (None, 2),
        (2, None),
    ],
)
def test_invalid_division_types(a, b):
    with pytest.raises((TypeError, ValueError)):
        divide(a, b)