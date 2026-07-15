"""
Centralized application configuration.

This module loads environment-specific settings from environment variables
or uses sensible defaults. All URLs, timeouts, and configuration should be
accessed through the Settings dataclass.

Usage:
    from config.settings import settings
    
    # Access settings
    api_url = settings.api_base_url
    timeout = settings.request_timeout
    headless_mode = settings.headless
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Application configuration loaded from environment variables.
    
    Immutable dataclass (frozen=True) ensures settings don't change during tests.
    All values have sensible defaults but can be overridden via environment variables.
    """
    
    # ========================================================================
    # API CONFIGURATION
    # ========================================================================
    
    api_base_url: str = os.getenv(
        "API_BASE_URL",
        "https://restful-booker.herokuapp.com"
    )
    """Base URL for REST API. Default: Restful-booker API"""
    
    # ========================================================================
    # UI CONFIGURATION
    # ========================================================================
    
    ui_base_url: str = os.getenv(
        "UI_BASE_URL",
        "https://automationintesting.online"
    )
    """Base URL for web application. Default: Automation testing site"""
    
    # ========================================================================
    # TIMEOUT CONFIGURATION (seconds)
    # ========================================================================
    
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    """HTTP request timeout in seconds"""
    
    page_load_timeout: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    """Browser page load timeout in seconds"""
    
    element_timeout: int = int(os.getenv("ELEMENT_TIMEOUT", "10"))
    """Element wait timeout in seconds"""
    
    # ========================================================================
    # BROWSER CONFIGURATION
    # ========================================================================
    
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    """Run browser in headless mode (no visible window)"""
    
    browser_type: str = os.getenv("BROWSER", "chromium")
    """Browser type: chromium, firefox, or webkit"""
    
    slow_motion: int = int(os.getenv("SLOWMO", "0"))
    """Slow down browser actions by N milliseconds"""
    
    # ========================================================================
    # ENVIRONMENT
    # ========================================================================
    
    environment: str = os.getenv("ENVIRONMENT", "local")
    """Environment: local, ci, staging, production"""
    
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    """Enable debug logging and verbose output"""
    
    # ========================================================================
    # TEST CONFIGURATION
    # ========================================================================
    
    retry_on_failure: int = int(os.getenv("RETRY_ON_FAILURE", "1"))
    """Number of times to retry failed tests"""
    
    parallel_workers: int = int(os.getenv("PARALLEL_WORKERS", "1"))
    """Number of parallel test workers"""
    
    # ========================================================================
    # OUTPUT CONFIGURATION
    # ========================================================================
    
    capture_screenshots: bool = os.getenv("CAPTURE_SCREENSHOTS", "true").lower() == "true"
    """Capture screenshots on test failure"""
    
    capture_video: bool = os.getenv("CAPTURE_VIDEO", "false").lower() == "true"
    """Record video of browser sessions"""
    
    def __str__(self) -> str:
        """Return human-readable configuration summary"""
        return (
            f"Settings(\n"
            f"  environment={self.environment}\n"
            f"  api_base_url={self.api_base_url}\n"
            f"  ui_base_url={self.ui_base_url}\n"
            f"  headless={self.headless}\n"
            f"  browser={self.browser_type}\n"
            f"  request_timeout={self.request_timeout}s\n"
            f"  page_load_timeout={self.page_load_timeout}s\n"
            f")"
        )


# Create singleton instance - use this everywhere
settings = Settings()


# ============================================================================
# FOR DEBUGGING - Print settings when module is imported in debug mode
# ============================================================================

if __name__ == "__main__":
    print("📋 Current Settings")
    print(settings)
    print("\n📍 Environment Variables:")
    print(f"  API_BASE_URL: {os.getenv('API_BASE_URL', '(using default)')}")
    print(f"  UI_BASE_URL: {os.getenv('UI_BASE_URL', '(using default)')}")
    print(f"  ENVIRONMENT: {os.getenv('ENVIRONMENT', '(using default)')}")
    print(f"  HEADLESS: {os.getenv('HEADLESS', '(using default)')}")
    print(f"  BROWSER: {os.getenv('BROWSER', '(using default)')}")
