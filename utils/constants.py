"""
Centralized constants for QA automation framework.

This module contains all magic strings, URLs, credentials, and configuration
that shouldn't be hardcoded in tests. Makes tests more maintainable and easier
to update when environment changes.

Usage:
    from utils.constants import TEST_CREDENTIALS, URLS, TIMEOUTS
    
    def test_login():
        username = TEST_CREDENTIALS['admin']['username']
        password = TEST_CREDENTIALS['admin']['password']
"""

import os
from typing import Dict, Any


# ============================================================================
# TEST CREDENTIALS
# ============================================================================
# These are for the public test site. Never commit real credentials!

TEST_CREDENTIALS: Dict[str, Dict[str, str]] = {
    'admin': {
        'username': 'admin',
        'password': 'password',
        'email': 'admin@test.com',
    },
    'user': {
        'username': 'user@example.com',
        'password': 'Test1234!',
        'email': 'user@example.com',
    },
    'invalid': {
        'username': 'invalid_user',
        'password': 'wrong_password',
        'email': 'invalid@test.com',
    },
}


# ============================================================================
# URLS
# ============================================================================
# Centralize all URL endpoints. Switch between environments by changing one place.

URLS: Dict[str, str] = {
    # Main application URLs
    'api_base': os.getenv('API_BASE_URL', 'https://restful-booker.herokuapp.com'),
    'ui_base': os.getenv('UI_BASE_URL', 'https://automationintesting.online'),
    
    # API endpoints
    'api_auth': '/auth',
    'api_booking': '/booking',
    'api_health': '/actuator/health',
    
    # UI pages
    'login': '/',
    'booking': '/admin/bookings',
    'dashboard': '/admin',
}


# ============================================================================
# TIMEOUTS (in seconds)
# ============================================================================
# How long to wait for things to happen

TIMEOUTS: Dict[str, float] = {
    # API timeouts
    'api_request': float(os.getenv('API_TIMEOUT', 10)),
    'api_retry': float(os.getenv('API_RETRY_TIMEOUT', 30)),
    
    # Playwright timeouts (milliseconds in browser, seconds here)
    'page_load': float(os.getenv('PAGE_LOAD_TIMEOUT', 30)),
    'element_wait': float(os.getenv('ELEMENT_TIMEOUT', 10)),
    'navigation': float(os.getenv('NAVIGATION_TIMEOUT', 10)),
    'action': float(os.getenv('ACTION_TIMEOUT', 5)),
    
    # Test timeouts
    'test_max': float(os.getenv('TEST_MAX_TIMEOUT', 60)),
}


# ============================================================================
# HTTP STATUS CODES
# ============================================================================
# Common HTTP status codes for assertions

STATUS_CODES: Dict[str, int] = {
    # 2xx Success
    'OK': 200,
    'CREATED': 201,
    'ACCEPTED': 202,
    'NO_CONTENT': 204,
    
    # 3xx Redirection
    'MOVED_PERMANENTLY': 301,
    'FOUND': 302,
    'NOT_MODIFIED': 304,
    
    # 4xx Client Error
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'CONFLICT': 409,
    'GONE': 410,
    
    # 5xx Server Error
    'SERVER_ERROR': 500,
    'SERVICE_UNAVAILABLE': 503,
}


# ============================================================================
# ERROR MESSAGES
# ============================================================================
# Expected error messages from the application

ERROR_MESSAGES: Dict[str, str] = {
    # Authentication errors
    'INVALID_CREDENTIALS': 'Invalid credentials',
    'AUTH_REQUIRED': 'Authentication required',
    'TOKEN_EXPIRED': 'Token expired',
    'UNAUTHORIZED': 'Unauthorized',
    
    # Validation errors
    'REQUIRED_FIELD': 'This field is required',
    'INVALID_EMAIL': 'Invalid email format',
    'INVALID_DATE': 'Invalid date format',
    'INVALID_PRICE': 'Price must be positive',
    'INVALID_DATES_ORDER': 'Check-in must be before check-out',
    
    # Not found errors
    'NOT_FOUND': 'Not found',
    'BOOKING_NOT_FOUND': 'Booking not found',
    'USER_NOT_FOUND': 'User not found',
    
    # Conflict errors
    'ALREADY_EXISTS': 'Already exists',
    'DUPLICATE_BOOKING': 'Booking already exists',
}


# ============================================================================
# BOOKING DATA CONSTANTS
# ============================================================================
# Valid ranges and constraints for booking data

BOOKING_CONSTRAINTS: Dict[str, Any] = {
    # Name constraints
    'name_min_length': 1,
    'name_max_length': 100,
    
    # Price constraints
    'price_min': 0.00,
    'price_max': 999999.99,
    
    # Deposit constraints
    'deposit_required_min': 0.00,
    'deposit_required_max': 100.00,  # Percentage
    
    # Room number constraints
    'room_number_min': 1,
    'room_number_max': 999,
    
    # Guest count constraints
    'guest_count_min': 1,
    'guest_count_max': 10,
    
    # Notes constraints
    'notes_max_length': 1000,
}


# ============================================================================
# VALID BOOKING DATA RANGES
# ============================================================================

VALID_BOOKING_DATA: Dict[str, Any] = {
    'first_names': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
    'last_names': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'],
    'emails': [
        'john.smith@example.com',
        'jane.doe@test.com',
        'bob@booking.com',
        'alice.test@company.org',
    ],
    'phone_numbers': [
        '+1234567890',
        '555-1234',
        '(555) 123-4567',
        '+44 20 7946 0958',
    ],
    'valid_prices': [10.00, 50.00, 99.99, 500.00, 1000.00],
    'valid_deposits': [0.0, 10.0, 50.0, 100.0],
    'valid_room_numbers': [1, 2, 5, 10, 50, 100],
}


# ============================================================================
# INVALID BOOKING DATA (for negative testing)
# ============================================================================

INVALID_BOOKING_DATA: Dict[str, Any] = {
    'empty_names': ['', ' ', '\n', '\t'],
    'too_long_name': ['x' * 101, 'A' * 1000],
    'invalid_emails': [
        'notanemail',
        '@example.com',
        'user@',
        'user name@example.com',
        'user@.com',
    ],
    'negative_prices': [-1, -10.00, -999.99],
    'invalid_prices': [-0.01, -1000.00],
    'invalid_dates_order': {
        'checkin': '2025-12-31',
        'checkout': '2025-12-01',  # Before checkin
    },
    'past_dates': {
        'checkin': '2020-01-01',
        'checkout': '2020-01-02',
    },
}


# ============================================================================
# UI ELEMENTS & SELECTORS
# ============================================================================
# These can be overridden in specific page objects, but here are common ones

SELECTORS: Dict[str, str] = {
    # Common buttons
    'submit_button': 'button[type="submit"]',
    'cancel_button': 'button:has-text("Cancel")',
    'save_button': 'button:has-text("Save")',
    'delete_button': 'button:has-text("Delete")',
    'edit_button': 'button:has-text("Edit")',
    
    # Common form elements
    'input_text': 'input[type="text"]',
    'input_email': 'input[type="email"]',
    'input_password': 'input[type="password"]',
    'input_number': 'input[type="number"]',
    'input_date': 'input[type="date"]',
    
    # Common elements
    'error_message': '.error, .alert-danger, [role="alert"]',
    'success_message': '.success, .alert-success',
    'loading_spinner': '.spinner, .loader, [role="progressbar"]',
    'modal': '.modal, .dialog, [role="dialog"]',
}


# ============================================================================
# BROWSER CONFIGURATION
# ============================================================================

BROWSER_CONFIG: Dict[str, Any] = {
    # Browser type defaults
    'browser': os.getenv('BROWSER', 'chromium'),
    'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
    'slowmo': int(os.getenv('SLOWMO', 0)),  # Milliseconds
    
    # Browser viewport
    'viewport': {
        'width': int(os.getenv('VIEWPORT_WIDTH', 1920)),
        'height': int(os.getenv('VIEWPORT_HEIGHT', 1080)),
    },
    
    # Debugging
    'devtools': os.getenv('DEVTOOLS', 'false').lower() == 'true',
    'record_video': os.getenv('RECORD_VIDEO', 'false').lower() == 'true',
}


# ============================================================================
# TEST EXECUTION CONFIGURATION
# ============================================================================

TEST_CONFIG: Dict[str, Any] = {
    # Retry settings
    'retry_on_failure': int(os.getenv('RETRY_ON_FAILURE', 1)),
    'retry_delay': float(os.getenv('RETRY_DELAY', 1.0)),  # Seconds
    
    # Parallelization
    'parallel_workers': int(os.getenv('PARALLEL_WORKERS', 1)),
    
    # Output
    'verbose': os.getenv('VERBOSE', 'false').lower() == 'true',
    'capture_screenshots': os.getenv('CAPTURE_SCREENSHOTS', 'true').lower() == 'true',
    'capture_video': os.getenv('CAPTURE_VIDEO', 'false').lower() == 'true',
}


# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()

# Environment-specific settings
ENV_CONFIG = {
    'local': {
        'headless': False,
        'slowmo': 100,
    },
    'ci': {
        'headless': True,
        'slowmo': 0,
        'retry_on_failure': 2,
    },
    'staging': {
        'headless': True,
        'slowmo': 50,
    },
    'production': {
        'headless': True,
        'slowmo': 0,
        'retry_on_failure': 3,
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_env_config() -> Dict[str, Any]:
    """
    Get configuration for current environment.
    
    Returns environment-specific overrides for test settings.
    Useful for adjusting behavior in CI vs local development.
    """
    return ENV_CONFIG.get(ENVIRONMENT, ENV_CONFIG['local'])


def get_api_url(endpoint: str) -> str:
    """
    Build complete API URL.
    
    Args:
        endpoint: The endpoint path (e.g., '/booking', '/auth')
        
    Returns:
        Complete URL (e.g., 'https://api.example.com/booking')
    """
    base = URLS['api_base']
    # Remove leading/trailing slashes and rejoin
    base = base.rstrip('/')
    endpoint = endpoint.lstrip('/')
    return f"{base}/{endpoint}"


def get_ui_url(page: str = '') -> str:
    """
    Build complete UI URL.
    
    Args:
        page: The page path (e.g., 'login', 'booking'). If empty, returns base.
        
    Returns:
        Complete URL (e.g., 'https://example.com/booking')
    """
    base = URLS['ui_base']
    page = page.lstrip('/')
    if page:
        return f"{base.rstrip('/')}/{page}"
    return base


if __name__ == '__main__':
    # Quick verification script
    print("📋 Constants Loaded Successfully!")
    print(f"Environment: {ENVIRONMENT}")
    print(f"API Base: {URLS['api_base']}")
    print(f"UI Base: {URLS['ui_base']}")
    print(f"Test Credentials Available: {len(TEST_CREDENTIALS)} users")
    print(f"Timeouts Configured: {len(TIMEOUTS)} settings")
    print(f"Status Codes: {len(STATUS_CODES)}")
