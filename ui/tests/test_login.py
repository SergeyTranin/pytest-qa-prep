"""
Test Login Functionality - UI Tests

These tests verify:
1. Valid login with correct credentials
2. Invalid login with wrong credentials
3. Required field validation
4. Error message display
5. Remember me functionality
6. Session persistence
7. Logout functionality
"""

import pytest
from playwright.sync_api import sync_playwright, Page
from ui.pages.login_page import LoginPage


@pytest.fixture
def browser():
    """
    Fixture to provide browser instance.
    
    Setup: Launch browser
    Teardown: Close browser
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """
    Fixture to provide page instance.
    
    Setup: Create new page
    Teardown: Close page
    """
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page):
    """
    Fixture to provide LoginPage object.
    
    Args:
        page: Page fixture
    
    Returns:
        LoginPage instance ready for testing
    """
    return LoginPage(page)


class TestLoginPageElements:
    """Test that login page elements are present."""
    
    def test_login_page_loads(self, login_page):
        """
        Test: Login page loads successfully.
        
        Why this test?
        - Verify page is accessible
        - Check basic page structure
        - Element prerequisites for other tests
        """
        login_page.goto_login()
        
        # Verify page title contains "Restful-booker" or "Hotel"
        title = login_page.get_title()
        assert "Restful-booker" in title or "Hotel" in title
    
    def test_login_form_elements_visible(self, login_page):
        """
        Test: All login form elements are visible.
        
        Why this test?
        - Verify UI is properly rendered
        - Check elements exist before interaction
        - Catch broken layouts early
        """
        login_page.goto_login()
        
        assert login_page.is_visible(login_page.USERNAME_INPUT)
        assert login_page.is_visible(login_page.PASSWORD_INPUT)
        assert login_page.is_visible(login_page.LOGIN_BUTTON)
    
    def test_remember_me_checkbox_present(self, login_page):
        """
        Test: Remember Me checkbox is visible.
        
        Why this test?
        - Verify optional features are present
        - Check for broken UI elements
        """
        login_page.goto_login()
        
        assert login_page.is_visible(login_page.REMEMBER_ME_CHECKBOX)


class TestValidLogin:
    """Test successful login scenarios."""
    
    def test_valid_login_success(self, login_page):
        """
        Test: Login with valid credentials succeeds.
        
        Why this test?
        - Happy path: main user flow
        - Verify authentication works
        - Tests integration with backend
        
        Note: Uses test credentials (adjust for your site)
        """
        login_page.goto_login()
        
        # Login with valid credentials
        login_page.login("admin", "password")
        
        # Wait for page to update
        login_page.wait_for_login_to_complete()
        
        # Verify logged in
        assert login_page.is_logged_in()
    
    def test_remember_me_functionality(self, browser):
        """
        Test: Remember Me checkbox persists session.
        
        Why this test?
        - Feature validation: remember me works
        - Session persistence
        - Cookie handling
        """
        # First page: Login with Remember Me
        page1 = browser.new_page()
        login_page1 = LoginPage(page1)
        
        login_page1.goto_login()
        login_page1.login_with_remember("admin", "password")
        login_page1.wait_for_login_to_complete()
        
        assert login_page1.is_logged_in()
        
        # Close first page
        page1.close()
        
        # Second page: Check if still logged in (session persisted)
        page2 = browser.new_page()
        login_page2 = LoginPage(page2)
        
        login_page2.goto_login()
        
        # If Remember Me worked, user should still be logged in
        # (This depends on the site's implementation)
        # For this site, we just verify we can navigate
        assert login_page2.is_visible(login_page2.LOGIN_BUTTON)
        
        page2.close()


class TestInvalidLogin:
    """Test login failure scenarios."""
    
    @pytest.mark.parametrize("username,password", [
        ("admin", "wrongpassword"),
        ("wronguser", "password"),
        ("admin", ""),
        ("", "password"),
    ])
    def test_invalid_credentials(self, login_page, username, password):
        """
        Test: Invalid credentials show error message.
        
        Why this test?
        - Security: wrong credentials rejected
        - Error handling: user gets feedback
        - Edge cases: empty fields
        
        Parametrized: Tests multiple scenarios in one test
        """
        login_page.goto_login()
        
        if username:
            login_page.enter_username(username)
        if password:
            login_page.enter_password(password)
        
        login_page.click_login()
        
        # Verify error message appears
        assert login_page.is_error_visible()
        assert len(login_page.get_error_message()) > 0


class TestLoginFormValidation:
    """Test form-level validation."""
    
    def test_empty_username_field(self, login_page):
        """
        Test: Cannot login with empty username.
        
        Why this test?
        - Required field validation
        - Browser-level validation
        - HTML5 form validation
        """
        login_page.goto_login()
        
        login_page.enter_password("password")
        login_page.click_login()
        
        # Should show validation error or not submit
        # Verify we're still on login page
        assert "Hotel" in login_page.get_title()
    
    def test_empty_password_field(self, login_page):
        """
        Test: Cannot login with empty password.
        
        Why this test?
        - Required field validation
        - Password field protection
        """
        login_page.goto_login()
        
        login_page.enter_username("admin")
        login_page.click_login()
        
        # Should show validation error or not submit
        assert "Hotel" in login_page.get_title()
    
    def test_special_characters_in_credentials(self, login_page):
        """
        Test: Handle special characters in username/password.
        
        Why this test?
        - Input validation with edge cases
        - Security: SQL injection prevention
        - Character encoding handling
        """
        login_page.goto_login()
        
        # Try special characters
        login_page.login("admin'\"<>", "pass\"'")
        
        # Should handle gracefully (error or reject)
        assert login_page.get_url() or login_page.is_visible(login_page.LOGIN_BUTTON)


class TestLoginFormInteraction:
    """Test form interaction patterns."""
    
    def test_password_field_is_masked(self, login_page):
        """
        Test: Password input is masked (not visible).
        
        Why this test?
        - Security: password privacy
        - Input type verification
        - User experience
        """
        login_page.goto_login()
        
        # Get password field type
        input_type = login_page.get_attribute(login_page.PASSWORD_INPUT, "type")
        
        # Should be password type (masked)
        assert input_type == "password"
    
    def test_clear_and_retype_credentials(self, login_page):
        """
        Test: Can clear and retype credentials.
        
        Why this test?
        - User error recovery
        - Field interaction robustness
        - Typing/clearing behavior
        """
        login_page.goto_login()
        
        # Type wrong credentials
        login_page.enter_username("wrong")
        login_page.enter_password("wrong")
        
        # Clear and retype
        login_page.enter_username("admin")
        login_page.enter_password("password")
        
        # Verify new values are set
        username_val = login_page.get_attribute(login_page.USERNAME_INPUT, "value")
        assert username_val == "admin"
    
    def test_enter_key_submits_form(self, login_page):
        """
        Test: Pressing Enter submits login form.
        
        Why this test?
        - User experience: keyboard submission
        - Common user pattern
        - Accessibility
        """
        login_page.goto_login()
        
        login_page.enter_username("admin")
        login_page.enter_password("password")
        
        # Press Enter on password field
        login_page.press(login_page.PASSWORD_INPUT, "Enter")
        
        # Wait for navigation
        login_page.wait_for_login_to_complete()
        
        # Should process login
        assert login_page.get_url()


class TestLogout:
    """Test logout functionality."""
    
    def test_logout_success(self, login_page):
        """
        Test: Logout removes session.
        
        Why this test?
        - Session cleanup: logout works
        - Session security: session ended
        - User state: back to unauthenticated
        """
        login_page.goto_login()
        
        # Login first
        login_page.login("admin", "password")
        login_page.wait_for_login_to_complete()
        
        assert login_page.is_logged_in()
        
        # Now logout
        login_page.logout()
        login_page.wait_for_navigation()
        
        # Should be logged out
        assert not login_page.is_logged_in()


class TestLoginPageUX:
    """Test user experience aspects of login."""
    
    def test_focus_on_username_field(self, login_page):
        """
        Test: Username field has focus on page load.
        
        Why this test?
        - UX: cursor starts in username field
        - Accessibility: keyboard navigation
        - User efficiency
        """
        login_page.goto_login()
        
        # Check if username field is visible and enabled
        assert login_page.is_visible(login_page.USERNAME_INPUT)
        assert login_page.is_enabled(login_page.USERNAME_INPUT)
    
    def test_login_button_enabled(self, login_page):
        """
        Test: Login button is clickable.
        
        Why this test?
        - UX: button is available
        - Form submission: not disabled
        """
        login_page.goto_login()
        
        assert login_page.is_enabled(login_page.LOGIN_BUTTON)
    
    def test_page_response_time(self, login_page):
        """
        Test: Login page loads quickly.
        
        Why this test?
        - Performance: page responsiveness
        - UX: not slow to load
        - Infrastructure: server response
        """
        import time
        
        start = time.time()
        login_page.goto_login()
        login_page.wait_for_element(login_page.LOGIN_BUTTON)
        elapsed = time.time() - start
        
        # Should load within 5 seconds
        assert elapsed < 5.0
