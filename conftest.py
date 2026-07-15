"""
Root-level pytest configuration and fixtures.

This conftest.py is shared across all test layers (API, UI, legacy).
Layer-specific fixtures are in their own conftest.py files (ui/conftest.py, etc).

Fixtures here are available to all tests in the project.
"""

import pytest
import os
from typing import Dict, Any


# ============================================================================
# SESSION-LEVEL FIXTURES (run once per test session)
# ============================================================================

@pytest.fixture(scope="session")
def session_config() -> Dict[str, Any]:
    """
    Load configuration once for entire test session.
    
    Yields:
        Dictionary with session-wide settings
    """
    print("\n[session] Loading configuration")
    config = {
        "environment": os.getenv("ENVIRONMENT", "local"),
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "parallel_mode": os.getenv("CI", "false").lower() == "true",
    }
    yield config
    print("\n[session] Teardown complete")


# ============================================================================
# MODULE-LEVEL FIXTURES (run once per test module)
# ============================================================================

@pytest.fixture(scope="module")
def shared_dataset() -> list:
    """
    Build shared test dataset for module.
    
    Used for tests that need pre-existing data that's expensive to create.
    
    Yields:
        List of test data
    """
    print("\n[module] Building shared dataset")
    data = [1, 2, 3]
    yield data
    print("\n[module] Clearing dataset")


# ============================================================================
# PYTEST HOOKS (customize test behavior)
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    
    Called once at startup to register custom test markers.
    """
    config.addinivalue_line(
        "markers",
        "api: API test layer"
    )
    config.addinivalue_line(
        "markers",
        "ui: UI test layer"
    )
    config.addinivalue_line(
        "markers",
        "smoke: Quick critical-path tests"
    )
    config.addinivalue_line(
        "markers",
        "regression: Full regression suite"
    )
    config.addinivalue_line(
        "markers",
        "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers",
        "flaky: Tests that are sometimes unreliable"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test items after collection.
    
    Automatically mark tests based on their location:
    - Tests in api/ get @pytest.mark.api
    - Tests in ui/ get @pytest.mark.ui
    """
    for item in items:
        # Mark API tests
        if "api/tests" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        
        # Mark UI tests
        elif "ui/tests" in str(item.fspath):
            item.add_marker(pytest.mark.ui)


def pytest_addoption(parser):
    """
    Add custom command-line options for pytest.
    
    Example:
        pytest --environment staging
        pytest --no-headless  # Show browser
    """
    parser.addoption(
        "--environment",
        action="store",
        default=os.getenv("ENVIRONMENT", "local"),
        help="Test environment: local, ci, staging, production"
    )
    parser.addoption(
        "--verbose-logging",
        action="store_true",
        default=False,
        help="Enable verbose logging output"
    )


# ============================================================================
# SESSION MARKERS AND FILTERING
# ============================================================================

# Command-line shortcuts:
# pytest -m api              # Run only API tests
# pytest -m ui               # Run only UI tests
# pytest -m smoke            # Run only smoke tests
# pytest -m "not slow"       # Skip slow tests
# pytest -m "api and not slow"  # API tests, exclude slow ones

if __name__ == '__main__':
    print("✓ Root conftest.py loaded correctly")
