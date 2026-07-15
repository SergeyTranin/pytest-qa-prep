"""
Custom assertions for QA automation framework.

These assertions provide cleaner error messages and more expressive validation
than standard pytest assertions. Use these for domain-specific validations.

Usage:
    from utils.assertions import assert_close, assert_in_range, assert_valid_response
    
    assert_close(99.00, 99.001)  # Floating point comparison
    assert_in_range(price, 0, 1000)  # Range validation
    assert_valid_response(response)  # HTTP response validation
"""

from typing import Any, Dict, List, Optional


def assert_close(actual: float, expected: float, tol: float = 1e-6) -> None:
    """
    Assert two floats are close within tolerance.
    
    Useful for floating-point comparisons that fail with == due to precision.
    
    Args:
        actual: Actual value
        expected: Expected value
        tol: Tolerance (default 1e-6)
        
    Raises:
        AssertionError: If difference exceeds tolerance
        
    Example:
        >>> assert_close(99.00, 99.001, tol=0.01)  # Pass
        >>> assert_close(99.00, 99.1)  # Fail if tol too small
    """
    diff = abs(actual - expected)
    assert diff <= tol, f"Expected {expected}, got {actual} (diff {diff} > tol {tol})"


def assert_in_range(value: float, min_val: float, max_val: float) -> None:
    """
    Assert value is within range (inclusive).
    
    Args:
        value: Value to check
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
        
    Raises:
        AssertionError: If value outside range
        
    Example:
        >>> assert_in_range(50, 0, 100)  # Pass
        >>> assert_in_range(150, 0, 100)  # Fail
    """
    assert min_val <= value <= max_val, \
        f"Expected {value} to be in range [{min_val}, {max_val}]"


def assert_valid_price(price: float) -> None:
    """
    Assert price is valid (positive number).
    
    Args:
        price: Price to validate
        
    Raises:
        AssertionError: If price is negative or not a number
        
    Example:
        >>> assert_valid_price(99.99)  # Pass
        >>> assert_valid_price(-10)  # Fail
    """
    assert isinstance(price, (int, float)), f"Price must be number, got {type(price)}"
    assert price >= 0, f"Price must be positive, got {price}"


def assert_valid_email(email: str) -> None:
    """
    Assert email has valid format (basic check).
    
    Args:
        email: Email address to validate
        
    Raises:
        AssertionError: If email format invalid
        
    Example:
        >>> assert_valid_email("user@example.com")  # Pass
        >>> assert_valid_email("invalid-email")  # Fail
    """
    assert isinstance(email, str), f"Email must be string, got {type(email)}"
    assert '@' in email and '.' in email, f"Invalid email format: {email}"
    assert email.count('@') == 1, f"Email has multiple @: {email}"


def assert_response_success(response: Dict[str, Any], 
                           expected_status: int = 200) -> None:
    """
    Assert API response indicates success.
    
    Args:
        response: Response dict with 'status_code' or 'code' field
        expected_status: Expected HTTP status code (default 200)
        
    Raises:
        AssertionError: If response doesn't indicate success
        
    Example:
        >>> assert_response_success({'status_code': 200, 'data': {}})
        >>> assert_response_success({'code': 201}, expected_status=201)
    """
    # Handle different response formats
    status = response.get('status_code') or response.get('code')
    assert status == expected_status, \
        f"Expected status {expected_status}, got {status}"


def assert_response_error(response: Dict[str, Any],
                         expected_status: int = 400) -> None:
    """
    Assert API response indicates error.
    
    Args:
        response: Response dict with 'status_code' or 'code' field
        expected_status: Expected error status code (default 400)
        
    Raises:
        AssertionError: If response doesn't indicate expected error
        
    Example:
        >>> assert_response_error({'status_code': 404}, expected_status=404)
    """
    status = response.get('status_code') or response.get('code')
    assert status == expected_status, \
        f"Expected error status {expected_status}, got {status}"


def assert_has_keys(obj: Dict[str, Any], keys: List[str]) -> None:
    """
    Assert dictionary has all required keys.
    
    Args:
        obj: Dictionary to check
        keys: List of required keys
        
    Raises:
        AssertionError: If any key missing
        
    Example:
        >>> assert_has_keys({'id': 1, 'name': 'test'}, ['id', 'name'])
        >>> assert_has_keys({'id': 1}, ['id', 'missing'])  # Fail
    """
    missing = [k for k in keys if k not in obj]
    assert not missing, f"Missing keys in response: {missing}"


def assert_no_empty_fields(obj: Dict[str, Any], 
                           ignore_fields: Optional[List[str]] = None) -> None:
    """
    Assert dictionary has no empty/None values (except ignored fields).
    
    Args:
        obj: Dictionary to check
        ignore_fields: List of fields to skip validation
        
    Raises:
        AssertionError: If any field is empty/None
        
    Example:
        >>> assert_no_empty_fields({'id': 1, 'name': 'test'})
        >>> assert_no_empty_fields({'id': None})  # Fail
    """
    ignore_fields = ignore_fields or []
    
    for key, value in obj.items():
        if key in ignore_fields:
            continue
        assert value is not None and value != '', \
            f"Field '{key}' is empty or None: {value}"


def assert_is_subset(subset: Dict[str, Any], superset: Dict[str, Any]) -> None:
    """
    Assert all subset items exist in superset with same values.
    
    Useful for validating response contains expected data.
    
    Args:
        subset: Expected data
        superset: Actual response data
        
    Raises:
        AssertionError: If subset items don't match in superset
        
    Example:
        >>> assert_is_subset({'id': 1}, {'id': 1, 'name': 'test', 'extra': 'field'})
    """
    for key, expected_value in subset.items():
        actual_value = superset.get(key)
        assert actual_value == expected_value, \
            f"Mismatch for key '{key}': expected {expected_value}, got {actual_value}"


if __name__ == '__main__':
    # Quick examples
    print("✓ assert_close: ", end="")
    assert_close(99.00, 99.001, tol=0.01)
    print("PASS")
    
    print("✓ assert_in_range: ", end="")
    assert_in_range(50, 0, 100)
    print("PASS")
    
    print("✓ assert_valid_price: ", end="")
    assert_valid_price(99.99)
    print("PASS")
    
    print("✓ assert_valid_email: ", end="")
    assert_valid_email("test@example.com")
    print("PASS")
    
    print("✓ assert_has_keys: ", end="")
    assert_has_keys({'id': 1, 'name': 'test'}, ['id', 'name'])
    print("PASS")
    
    print("\n✅ All custom assertions working!")
