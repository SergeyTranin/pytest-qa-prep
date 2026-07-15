"""
Login Page - Handles user authentication

This page tests:
- User login with valid/invalid credentials
- Form submission
- Error message handling
- Session management
"""

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for login functionality.
    
    Locators:
    - Username field: input for email
    - Password field: input for password
    - Login button: button to submit
    - Error message: alert showing login errors
    - Remember me: checkbox to persist session
    """
    
    # Locators (CSS selectors for elements on the page)
    USERNAME_INPUT = 'input[id="username"]'
    PASSWORD_INPUT = 'input[id="password"]'
    LOGIN_BUTTON = 'button[type="submit"]'
    ERROR_MESSAGE = '.alert-danger'
    REMEMBER_ME_CHECKBOX = 'input[id="remember"]'
    LOGOUT_BUTTON = 'button[id="logout"]'
    USER_PROFILE_BUTTON = '.user-profile'
    
    def goto_login(self):
        """Navigate to login page."""
        self.goto(f"{self.base_url}/")
    
    def enter_username(self, username: str):
        """
        Enter username in the username field.
        
        Args:
            username: Email address or username
        """
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        """
        Enter password in the password field.
        
        Args:
            password: Password string
        """
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        """
        Perform complete login flow.
        
        Args:
            username: Email address or username
            password: Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def toggle_remember_me(self):
        """Toggle 'Remember Me' checkbox."""
        self.click(self.REMEMBER_ME_CHECKBOX)
    
    def is_remember_me_checked(self) -> bool:
        """Check if 'Remember Me' is checked."""
        return self.is_checked(self.REMEMBER_ME_CHECKBOX)
    
    def login_with_remember(self, username: str, password: str):
        """
        Login with 'Remember Me' checked.
        
        Args:
            username: Email address or username
            password: Password
        """
        self.enter_username(username)
        self.enter_password(password)
        
        if not self.is_remember_me_checked():
            self.toggle_remember_me()
        
        self.click_login()
    
    def get_error_message(self) -> str:
        """
        Get error message if login fails.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        """Check if error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def is_logged_in(self) -> bool:
        """
        Verify user is logged in.
        
        Returns:
            True if logged in (profile visible), False otherwise
        """
        try:
            return self.is_visible(self.USER_PROFILE_BUTTON)
        except Exception:
            return False
    
    def logout(self):
        """Click logout button."""
        self.click(self.LOGOUT_BUTTON)
    
    def wait_for_login_page(self):
        """Wait for login page to load."""
        self.wait_for_element(self.LOGIN_BUTTON)
    
    def wait_for_login_to_complete(self):
        """Wait for login to complete (redirect)."""
        self.wait_for_navigation()
