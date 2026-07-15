def assert_close(actual: float, expected: float, tol: float = 1e-6):
    diff = abs(actual - expected)
    assert diff <= tol, f"Expected {expected}, got {actual} (diff {diff} > tol {tol})"
