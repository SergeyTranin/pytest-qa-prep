"""
Booking Page - Handles hotel booking interactions

This page tests:
- Viewing available bookings
- Creating new bookings
- Editing bookings
- Canceling bookings
- Form validation
"""

from ui.pages.base_page import BasePage
from typing import List, Dict


class BookingPage(BasePage):
    """
    Page Object for booking management.
    
    Locators:
    - Booking list: table of bookings
    - Create booking button: button to create new booking
    - First name field: input for guest first name
    - Last name field: input for guest last name
    - Price field: input for booking price
    - Deposit paid checkbox: toggle for deposit
    - Check-in date: date picker for check-in
    - Check-out date: date picker for check-out
    - Additional needs: text area for special requests
    - Submit button: save booking
    - Edit button: edit existing booking
    - Delete button: delete booking
    - Success message: booking confirmed
    """
    
    # Locators for booking list
    BOOKING_TABLE = 'table'
    BOOKING_ROWS = 'table tbody tr'
    BOOKING_ID_CELL = 'td:nth-child(1)'
    
    # Locators for booking form
    FIRST_NAME_INPUT = 'input[id="firstname"]'
    LAST_NAME_INPUT = 'input[id="lastname"]'
    TOTAL_PRICE_INPUT = 'input[id="totalprice"]'
    DEPOSIT_PAID_CHECKBOX = 'input[id="depositpaid"]'
    CHECKIN_DATE = 'input[id="checkin"]'
    CHECKOUT_DATE = 'input[id="checkout"]'
    ADDITIONAL_NEEDS = 'textarea[id="additionalneeds"]'
    
    # Locators for form actions
    SAVE_BOOKING_BUTTON = 'button#savebooking'
    EDIT_BOOKING_BUTTON = 'button#editbooking'
    DELETE_BOOKING_BUTTON = 'button#deletebooking'
    CREATE_BOOKING_BUTTON = 'button#createbooking'
    CANCEL_BUTTON = 'button#cancel'
    
    # Locators for feedback
    SUCCESS_MESSAGE = '.alert-success'
    ERROR_MESSAGE = '.alert-danger'
    BOOKING_ID_OUTPUT = 'p#bookingid'
    
    def goto_bookings(self):
        """Navigate to bookings page."""
        self.goto(f"{self.base_url}/#/admin/bookings")
    
    def click_create_booking(self):
        """Click create new booking button."""
        self.click(self.CREATE_BOOKING_BUTTON)
    
    def enter_first_name(self, firstname: str):
        """
        Enter guest first name.
        
        Args:
            firstname: First name
        """
        self.fill(self.FIRST_NAME_INPUT, firstname)
    
    def enter_last_name(self, lastname: str):
        """
        Enter guest last name.
        
        Args:
            lastname: Last name
        """
        self.fill(self.LAST_NAME_INPUT, lastname)
    
    def enter_total_price(self, price: str):
        """
        Enter booking price.
        
        Args:
            price: Price amount
        """
        self.fill(self.TOTAL_PRICE_INPUT, price)
    
    def toggle_deposit_paid(self):
        """Toggle deposit paid checkbox."""
        self.click(self.DEPOSIT_PAID_CHECKBOX)
    
    def is_deposit_paid_checked(self) -> bool:
        """Check if deposit paid is checked."""
        return self.is_checked(self.DEPOSIT_PAID_CHECKBOX)
    
    def enter_checkin_date(self, date: str):
        """
        Enter check-in date.
        
        Args:
            date: Date string (format depends on site)
        """
        self.fill(self.CHECKIN_DATE, date)
    
    def enter_checkout_date(self, date: str):
        """
        Enter check-out date.
        
        Args:
            date: Date string
        """
        self.fill(self.CHECKOUT_DATE, date)
    
    def enter_additional_needs(self, needs: str):
        """
        Enter additional special requests.
        
        Args:
            needs: Special requests text
        """
        self.fill(self.ADDITIONAL_NEEDS, needs)
    
    def save_booking(self):
        """Click save booking button."""
        self.click(self.SAVE_BOOKING_BUTTON)
    
    def create_complete_booking(
        self,
        firstname: str,
        lastname: str,
        price: str,
        checkin: str,
        checkout: str,
        deposit_paid: bool = True,
        additional_needs: str = None
    ):
        """
        Create a complete booking by filling all fields.
        
        Args:
            firstname: Guest first name
            lastname: Guest last name
            price: Total price
            checkin: Check-in date
            checkout: Check-out date
            deposit_paid: Whether deposit is paid
            additional_needs: Special requests (optional)
        """
        self.enter_first_name(firstname)
        self.enter_last_name(lastname)
        self.enter_total_price(price)
        
        if deposit_paid and not self.is_deposit_paid_checked():
            self.toggle_deposit_paid()
        elif not deposit_paid and self.is_deposit_paid_checked():
            self.toggle_deposit_paid()
        
        self.enter_checkin_date(checkin)
        self.enter_checkout_date(checkout)
        
        if additional_needs:
            self.enter_additional_needs(additional_needs)
        
        self.save_booking()
    
    def get_success_message(self) -> str:
        """Get success message after booking."""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_success_visible(self) -> bool:
        """Check if success message is visible."""
        return self.is_visible(self.SUCCESS_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get error message if booking fails."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        """Check if error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def get_booking_id(self) -> str:
        """
        Get the booking ID after creation.
        
        Returns:
            Booking ID
        """
        return self.get_text(self.BOOKING_ID_OUTPUT)
    
    def get_booking_count(self) -> int:
        """
        Get number of bookings in the list.
        
        Returns:
            Count of bookings
        """
        return self.find_elements(self.BOOKING_ROWS).count()
    
    def get_all_booking_ids(self) -> List[str]:
        """
        Get all booking IDs from the table.
        
        Returns:
            List of booking ID strings
        """
        rows = self.find_elements(self.BOOKING_ROWS)
        booking_ids = []
        
        for i in range(rows.count()):
            row = rows.nth(i)
            booking_id = row.locator(self.BOOKING_ID_CELL).text_content()
            booking_ids.append(booking_id.strip())
        
        return booking_ids
    
    def click_edit_booking(self, booking_id: str = None):
        """
        Click edit button for a booking.
        
        Args:
            booking_id: ID of booking to edit (optional)
        """
        if booking_id:
            # Find and click edit button for specific booking
            rows = self.find_elements(self.BOOKING_ROWS)
            for i in range(rows.count()):
                row = rows.nth(i)
                id_text = row.locator(self.BOOKING_ID_CELL).text_content()
                if booking_id in id_text:
                    row.locator('button').first.click()
                    return
        else:
            # Click first edit button
            self.click(self.EDIT_BOOKING_BUTTON)
    
    def delete_booking(self, booking_id: str = None):
        """
        Delete a booking.
        
        Args:
            booking_id: ID of booking to delete (optional)
        """
        if booking_id:
            # Find and click delete button for specific booking
            rows = self.find_elements(self.BOOKING_ROWS)
            for i in range(rows.count()):
                row = rows.nth(i)
                id_text = row.locator(self.BOOKING_ID_CELL).text_content()
                if booking_id in id_text:
                    buttons = row.locator('button')
                    buttons.nth(1).click()  # Delete is usually second button
                    return
        else:
            # Click delete button
            self.click(self.DELETE_BOOKING_BUTTON)
    
    def cancel_booking_edit(self):
        """Cancel booking edit."""
        self.click(self.CANCEL_BUTTON)
    
    def wait_for_bookings_table(self):
        """Wait for bookings table to load."""
        self.wait_for_element(self.BOOKING_TABLE)
