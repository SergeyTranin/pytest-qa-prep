import pytest
from calculator import add, subtract, multiply, divide

# positive cases
def test_add():
    assert add(1, 2) == 3
def test_subtract():
    assert subtract(183, 200) == -17
    assert subtract(999, 123) == 876
def test_multiply():
    assert multiply(13, 7) == 91
def test_divide():
    assert divide(100, 2) == 50
def test_divide_returns_float():
    assert divide(5, 2) == 2.5

# negative cases
def test_divide_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(100, 0)
def test_divide_negative():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(-100, 0)

# edge cases
def test_multiply_zero():
    assert multiply(0, 0) == 0
def test_multiply_negative():
    assert multiply(-100, 0) == 0