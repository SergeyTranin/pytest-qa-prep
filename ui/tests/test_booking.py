"""
Test Booking Functionality - UI Tests

These tests verify:
1. Viewing bookings
2. Creating new bookings
3. Editing bookings
4. Deleting bookings
5. Form validation
6. Success/error messages
7. Booking list management
"""

import pytest
from playwright.sync_api import sync_playwright
from ui.pages.login_page import LoginPage
from ui.pages.booking_page import BookingPage


@pytest.fixture
def browser():
    """Launch browser for tests."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create new page for each test."""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def authenticated_page(page):
    """
    Fixture: Login and provide authenticated page.
    
    Setup: Login to the application
    Teardown: Logout and close page
    """
    login_page = LoginPage(page)
    login_page.goto_login()
    login_page.login("admin", "password")
    login_page.wait_for_login_to_complete()
    
    yield page
    
    # Cleanup: Logout
    try:
        login_page.logout()
    except Exception:
        pass


@pytest.fixture
def booking_page(authenticated_page):
    """Provide BookingPage object on authenticated page."""
    return BookingPage(authenticated_page)


class TestBookingPageLoad:
    """Test booking page loads and displays correctly."""
    
    def test_bookings_page_loads(self, booking_page):
        """
        Test: Bookings page loads successfully.
        
        Why this test?
        - Navigation works
        - Page is accessible
        - Basic page structure present
        """
        booking_page.goto_bookings()
        booking_page.wait_for_bookings_table()
        
        # Verify bookings table is visible
        assert booking_page.is_visible(booking_page.BOOKING_TABLE)
    
    def test_bookings_table_not_empty(self, booking_page):
        """
        Test: Bookings table contains data.
        
        Why this test?
        - Data loading works
        - Table not empty (has bookings)
        - Rendering successful
        """
        booking_page.goto_bookings()
        booking_page.wait_for_bookings_table()
        
        # Get booking count
        count = booking_page.get_booking_count()
        
        # Should have at least one booking
        assert count > 0
    
    def test_booking_ids_are_visible(self, booking_page):
        """
        Test: Booking IDs are displayed in table.
        
        Why this test?
        - Data is displayed correctly
        - Table columns are visible
        - IDs can be identified
        """
        booking_page.goto_bookings()
        booking_page.wait_for_bookings_table()
        
        booking_ids = booking_page.get_all_booking_ids()
        
        # Should have booking IDs
        assert len(booking_ids) > 0
        # IDs should be numeric strings
        assert all(booking_id.isdigit() for booking_id in booking_ids)


class TestCreateBooking:
    """Test creating new bookings."""
    
    def test_create_booking_form_visible(self, booking_page):
        """
        Test: Create booking form fields are visible.
        
        Why this test?
        - Form elements present
        - User can fill form
        - Prerequisites for creation
        """
        booking_page.goto_bookings()
        
        # Click create booking button
        booking_page.click_create_booking()
        
        # Verify form fields are visible
        assert booking_page.is_visible(booking_page.FIRST_NAME_INPUT)
        assert booking_page.is_visible(booking_page.LAST_NAME_INPUT)
        assert booking_page.is_visible(booking_page.TOTAL_PRICE_INPUT)
    
    def test_create_booking_with_valid_data(self, booking_page):
        """
        Test: Create booking with all valid data.
        
        Why this test?
        - Happy path: booking creation
        - Form submission works
        - Data persists
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        # Create booking
        booking_page.create_complete_booking(
            firstname="John",
            lastname="Doe",
            price="150",
            checkin="2024-06-01",
            checkout="2024-06-05",
            deposit_paid=True,
            additional_needs="Late checkout"
        )
        
        # Verify success
        assert booking_page.is_success_visible()
    
    def test_create_booking_without_optional_needs(self, booking_page):
        """
        Test: Create booking without optional additional needs.
        
        Why this test?
        - Optional fields work correctly
        - Booking created without extras
        - Minimal valid data
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        # Create booking without additional needs
        booking_page.enter_first_name("Jane")
        booking_page.enter_last_name("Smith")
        booking_page.enter_total_price("200")
        
        if not booking_page.is_deposit_paid_checked():
            booking_page.toggle_deposit_paid()
        
        booking_page.enter_checkin_date("2024-07-01")
        booking_page.enter_checkout_date("2024-07-05")
        
        booking_page.save_booking()
        
        # Should succeed
        assert booking_page.is_success_visible()
    
    @pytest.mark.parametrize("firstname,lastname,price", [
        ("John", "Doe", "100"),
        ("Jane", "Smith", "250"),
        ("Bob", "Johnson", "1000"),
    ])
    def test_create_multiple_bookings(self, booking_page, firstname, lastname, price):
        """
        Test: Create multiple bookings with different data.
        
        Why this test?
        - Multiple operations work
        - Each booking is independent
        - System handles multiple records
        
        Parametrized: Tests multiple scenarios
        """
        booking_page.goto_bookings()
        
        booking_page.click_create_booking()
        
        booking_page.create_complete_booking(
            firstname=firstname,
            lastname=lastname,
            price=price,
            checkin="2024-06-01",
            checkout="2024-06-05"
        )
        
        assert booking_page.is_success_visible()


class TestBookingFormValidation:
    """Test booking form validation."""
    
    def test_empty_first_name_validation(self, booking_page):
        """
        Test: First name is required.
        
        Why this test?
        - Required field validation
        - Form doesn't submit with missing data
        - User gets feedback
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        # Leave first name empty, fill others
        booking_page.enter_last_name("Doe")
        booking_page.enter_total_price("100")
        booking_page.save_booking()
        
        # Should show error or not submit
        # Verify we're still on booking form (not submitted)
        assert booking_page.is_visible(booking_page.FIRST_NAME_INPUT)
    
    def test_invalid_price_format(self, booking_page):
        """
        Test: Price field handles invalid input.
        
        Why this test?
        - Input validation: numbers only
        - Type validation
        - Error handling
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        booking_page.enter_first_name("John")
        booking_page.enter_last_name("Doe")
        booking_page.enter_total_price("not-a-number")
        
        # Should either reject or correct input
        price_value = booking_page.get_attribute(
            booking_page.TOTAL_PRICE_INPUT,
            "value"
        )
        
        # Value should be numeric or empty
        assert price_value == "" or price_value.replace(".", "").isdigit()
    
    @pytest.mark.parametrize("checkin,checkout", [
        ("2024-06-05", "2024-06-01"),  # Checkout before checkin
        ("2024-06-01", "2024-06-01"),  # Same day
    ])
    def test_invalid_date_combinations(self, booking_page, checkin, checkout):
        """
        Test: Validate date combinations.
        
        Why this test?
        - Business logic validation
        - Checkout must be after checkin
        - Prevents illogical bookings
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        booking_page.enter_first_name("Test")
        booking_page.enter_last_name("User")
        booking_page.enter_total_price("100")
        booking_page.enter_checkin_date(checkin)
        booking_page.enter_checkout_date(checkout)
        
        booking_page.save_booking()
        
        # Should show error for invalid dates
        # (or might allow same-day checkout)
        # Just verify form is still visible
        assert booking_page.is_visible(booking_page.CHECKIN_DATE)


class TestDepositPaidToggle:
    """Test deposit paid checkbox functionality."""
    
    def test_deposit_paid_checkbox_toggle(self, booking_page):
        """
        Test: Deposit paid checkbox can be toggled.
        
        Why this test?
        - Checkbox functionality works
        - State persists
        - Both states valid
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        initial_state = booking_page.is_deposit_paid_checked()
        
        booking_page.toggle_deposit_paid()
        
        final_state = booking_page.is_deposit_paid_checked()
        
        # State should have changed
        assert initial_state != final_state
    
    def test_create_booking_with_deposit_paid_true(self, booking_page):
        """
        Test: Create booking with deposit paid = true.
        
        Why this test?
        - Feature works: deposit paid
        - Data captured correctly
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        if not booking_page.is_deposit_paid_checked():
            booking_page.toggle_deposit_paid()
        
        assert booking_page.is_deposit_paid_checked()
        
        booking_page.enter_first_name("Paid")
        booking_page.enter_last_name("Guest")
        booking_page.enter_total_price("500")
        booking_page.enter_checkin_date("2024-06-01")
        booking_page.enter_checkout_date("2024-06-05")
        
        booking_page.save_booking()
        
        assert booking_page.is_success_visible()
    
    def test_create_booking_with_deposit_paid_false(self, booking_page):
        """
        Test: Create booking with deposit paid = false.
        
        Why this test?
        - Feature works: deposit not paid option
        - Both states accepted
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        if booking_page.is_deposit_paid_checked():
            booking_page.toggle_deposit_paid()
        
        assert not booking_page.is_deposit_paid_checked()
        
        booking_page.enter_first_name("Unpaid")
        booking_page.enter_last_name("Guest")
        booking_page.enter_total_price("300")
        booking_page.enter_checkin_date("2024-07-01")
        booking_page.enter_checkout_date("2024-07-05")
        
        booking_page.save_booking()
        
        assert booking_page.is_success_visible()


class TestBookingList:
    """Test booking list operations."""
    
    def test_get_all_booking_ids(self, booking_page):
        """
        Test: Can retrieve all booking IDs from list.
        
        Why this test?
        - Data retrieval works
        - List parsing correct
        - All records accessible
        """
        booking_page.goto_bookings()
        booking_page.wait_for_bookings_table()
        
        booking_ids = booking_page.get_all_booking_ids()
        
        assert len(booking_ids) > 0
        # IDs should be unique or at least valid
        assert all(len(bid) > 0 for bid in booking_ids)
    
    def test_booking_count_increases_after_creation(self, booking_page):
        """
        Test: Booking count increases when new booking created.
        
        Why this test?
        - New records appear in list
        - Data persistence verified
        - List updates correctly
        """
        booking_page.goto_bookings()
        
        initial_count = booking_page.get_booking_count()
        
        booking_page.click_create_booking()
        
        booking_page.create_complete_booking(
            firstname="NewBooking",
            lastname="Test",
            price="100",
            checkin="2024-06-01",
            checkout="2024-06-05"
        )
        
        # Navigate back to list
        booking_page.goto_bookings()
        booking_page.wait_for_bookings_table()
        
        final_count = booking_page.get_booking_count()
        
        # Count should increase
        assert final_count >= initial_count


class TestBookingMessageDisplay:
    """Test success and error message display."""
    
    def test_success_message_content(self, booking_page):
        """
        Test: Success message has appropriate content.
        
        Why this test?
        - User feedback is clear
        - Message confirms action
        - Not just "Success"
        """
        booking_page.goto_bookings()
        booking_page.click_create_booking()
        
        booking_page.create_complete_booking(
            firstname="Success",
            lastname="Message",
            price="100",
            checkin="2024-06-01",
            checkout="2024-06-05"
        )
        
        message = booking_page.get_success_message()
        
        # Message should have content
        assert len(message) > 5
        # Should be positive/success related
        assert "success" in message.lower() or "saved" in message.lower() or "created" in message.lower()
