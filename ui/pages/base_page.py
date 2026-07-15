"""
Base Page Object Model - Foundation for all page interactions

This class provides common methods that all pages share:
- Navigation
- Element finding
- Waiting for elements
- Screenshots

Page Object Model (POM) Pattern:
- Each page has its own class
- Locators are defined as class variables
- Page methods mirror user actions (login, submit_form, etc.)
- Tests use page methods, not raw element interactions

Benefits:
- Maintainable: Change locator in one place
- Readable: Tests look like scenarios
- Reusable: Methods can be shared
"""

from playwright.sync_api import Page
from config.settings import settings


class BasePage:
    """
    Base class for all page objects.
    
    Provides common functionality:
    - Navigation
    - Element interaction
    - Waiting and assertions
    - Screenshots for debugging
    """
    
    def __init__(self, page: Page):
        """
        Initialize page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.base_url = settings.ui_base_url
    
    def goto(self, url: str = None):
        """
        Navigate to a URL.
        
        Args:
            url: Full URL or path. If None, uses page's default URL.
        """
        if url is None:
            url = self.base_url
        
        self.page.goto(url)
    
    def find_element(self, locator: str):
        """
        Find a single element by locator.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            Locator object for interaction
        """
        return self.page.locator(locator)
    
    def find_elements(self, locator: str):
        """
        Find multiple elements by locator.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            Locator object (can iterate or get count)
        """
        return self.page.locator(locator)
    
    def click(self, locator: str):
        """
        Click an element.
        
        Args:
            locator: CSS selector or XPath
        """
        self.page.click(locator)
    
    def fill(self, locator: str, value: str):
        """
        Fill a text input field.
        
        Args:
            locator: CSS selector or XPath
            value: Text to enter
        """
        self.page.fill(locator, value)
    
    def type(self, locator: str, value: str, delay: int = 50):
        """
        Type text character by character (slower, more human-like).
        
        Args:
            locator: CSS selector or XPath
            value: Text to type
            delay: Milliseconds between characters
        """
        self.page.locator(locator).type(value, delay=delay)
    
    def press(self, locator: str, key: str):
        """
        Press a key on an element.
        
        Args:
            locator: CSS selector or XPath
            key: Key name (Enter, Escape, ArrowDown, etc.)
        """
        self.page.locator(locator).press(key)
    
    def select_option(self, locator: str, value: str):
        """
        Select option from dropdown.
        
        Args:
            locator: CSS selector for <select>
            value: Option value to select
        """
        self.page.select_option(locator, value)
    
    def get_text(self, locator: str) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            Element text
        """
        return self.page.locator(locator).text_content()
    
    def get_attribute(self, locator: str, attribute: str) -> str:
        """
        Get attribute value.
        
        Args:
            locator: CSS selector or XPath
            attribute: Attribute name
        
        Returns:
            Attribute value
        """
        return self.page.locator(locator).get_attribute(attribute)
    
    def is_visible(self, locator: str) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            True if visible, False otherwise
        """
        return self.page.locator(locator).is_visible()
    
    def is_enabled(self, locator: str) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            True if enabled, False otherwise
        """
        return self.page.locator(locator).is_enabled()
    
    def is_checked(self, locator: str) -> bool:
        """
        Check if checkbox/radio is checked.
        
        Args:
            locator: CSS selector or XPath
        
        Returns:
            True if checked, False otherwise
        """
        return self.page.locator(locator).is_checked()
    
    def wait_for_element(self, locator: str, timeout: int = 5000):
        """
        Wait for element to appear.
        
        Args:
            locator: CSS selector or XPath
            timeout: Milliseconds to wait
        """
        self.page.locator(locator).wait_for(timeout=timeout)
    
    def wait_for_navigation(self, timeout: int = 30000):
        """
        Wait for page navigation to complete.
        
        Args:
            timeout: Milliseconds to wait
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get current URL."""
        return self.page.url
    
    def screenshot(self, name: str = "screenshot.png"):
        """
        Take screenshot for debugging.
        
        Args:
            name: Screenshot filename
        """
        self.page.screenshot(path=f"screenshots/{name}")
    
    def go_back(self):
        """Navigate back."""
        self.page.go_back()
    
    def go_forward(self):
        """Navigate forward."""
        self.page.go_forward()
    
    def reload(self):
        """Reload page."""
        self.page.reload()
    
    def close(self):
        """Close page."""
        self.page.close()
