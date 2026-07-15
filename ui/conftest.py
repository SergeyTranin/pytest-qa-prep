"""
Pytest Configuration for UI Tests

This file sets up:
- Browser fixtures
- Page fixtures
- Logging and reporting
- Test markers
"""

import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (show browser)"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to use: chromium, firefox, or webkit"
    )


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "login: mark test as login-related"
    )
    config.addinivalue_line(
        "markers",
        "booking: mark test as booking-related"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers",
        "smoke: mark test as smoke test (quick basic checks)"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """Configure browser launch arguments."""
    return {
        "headless": not pytestconfig.getoption("--headed")
    }


@pytest.fixture
def playwright_instance():
    """Provide Playwright instance."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture
def browser(request, playwright_instance):
    """
    Provide browser instance.
    
    Can be configured via:
    - pytest --browser firefox  (choose browser)
    - pytest --headed (show browser window)
    """
    browser_name = request.config.getoption("--browser")
    
    if browser_name == "chromium":
        browser = playwright_instance.chromium
    elif browser_name == "firefox":
        browser = playwright_instance.firefox
    elif browser_name == "webkit":
        browser = playwright_instance.webkit
    else:
        raise ValueError(f"Unknown browser: {browser_name}")
    
    launched_browser = browser.launch(
        headless=not request.config.getoption("--headed")
    )
    
    yield launched_browser
    
    launched_browser.close()


@pytest.fixture
def context(browser):
    """Provide browser context (isolated cookies/storage)."""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context):
    """
    Provide page instance.
    
    Each test gets a fresh page with:
    - No cookies from other tests
    - Clean storage
    - Fresh session
    """
    page = context.new_page()
    
    yield page
    
    page.close()


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(page, request):
    """
    Take screenshot when test fails.
    
    Automatically captures browser state for debugging.
    """
    yield
    
    if hasattr(request, 'node') and hasattr(request.node, 'rep_call'):
        if request.node.rep_call.failed:
            test_name = request.node.name
            page.screenshot(path=f"screenshots/{test_name}.png")
