"""
Generate realistic test data for QA automation.

This module creates valid and invalid test data for parametrized tests.
Replaces hardcoded test data and makes tests more maintainable.

Usage:
    from utils.data_generator import BookingDataGenerator, DataGenerator
    
    # Generate valid booking data
    booking_data = BookingDataGenerator.valid_booking()
    
    # Generate invalid data for negative testing
    invalid_email = DataGenerator.invalid_email()
    
    # Use in parametrized tests
    @pytest.mark.parametrize('email', DataGenerator.invalid_emails(5))
    def test_invalid_email(email):
        assert validate_email(email) is False
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from utils.constants import (
    VALID_BOOKING_DATA,
    INVALID_BOOKING_DATA,
    BOOKING_CONSTRAINTS,
)


class DataGenerator:
    """
    Generate random test data for validation and parametrization.
    
    Provides methods to generate realistic data for testing various scenarios.
    All methods are static and can be called without instantiation.
    """
    
    @staticmethod
    def random_string(length: int = 10, chars: str = string.ascii_letters) -> str:
        """
        Generate random string of specified length.
        
        Args:
            length: Length of string to generate (default 10)
            chars: Character set to use (default lowercase + uppercase)
            
        Returns:
            Random string
            
        Example:
            >>> s = DataGenerator.random_string(5)
            >>> len(s) == 5
            True
        """
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def random_number(min_val: int = 0, max_val: int = 1000) -> int:
        """
        Generate random integer within range.
        
        Args:
            min_val: Minimum value (inclusive, default 0)
            max_val: Maximum value (inclusive, default 1000)
            
        Returns:
            Random integer within range
        """
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_float(min_val: float = 0.0, max_val: float = 1000.0, decimals: int = 2) -> float:
        """
        Generate random float within range.
        
        Args:
            min_val: Minimum value (inclusive, default 0.0)
            max_val: Maximum value (inclusive, default 1000.0)
            decimals: Number of decimal places (default 2)
            
        Returns:
            Random float rounded to specified decimals
            
        Example:
            >>> price = DataGenerator.random_float(10.0, 500.0)
            >>> 10.0 <= price <= 500.0
            True
        """
        value = random.uniform(min_val, max_val)
        return round(value, decimals)
    
    @staticmethod
    def random_choice(items: List[Any]) -> Any:
        """
        Pick random item from list.
        
        Args:
            items: List to choose from
            
        Returns:
            Randomly selected item
        """
        return random.choice(items)
    
    @staticmethod
    def random_email(domain: str = 'test.com') -> str:
        """
        Generate random email address.
        
        Args:
            domain: Email domain (default 'test.com')
            
        Returns:
            Random email address
            
        Example:
            >>> email = DataGenerator.random_email()
            >>> '@' in email and 'test.com' in email
            True
        """
        username = DataGenerator.random_string(10, string.ascii_lowercase + string.digits)
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone(country_code: str = '+1') -> str:
        """
        Generate random phone number.
        
        Args:
            country_code: Country code prefix (default '+1' for US)
            
        Returns:
            Random phone number
        """
        number = ''.join(str(random.randint(0, 9)) for _ in range(10))
        return f"{country_code}{number}"
    
    @staticmethod
    def invalid_email() -> str:
        """
        Generate one invalid email address.
        
        Returns:
            Invalid email that should fail validation
        """
        return random.choice(INVALID_BOOKING_DATA['invalid_emails'])
    
    @staticmethod
    def invalid_emails(count: int = 5) -> List[str]:
        """
        Generate multiple invalid email addresses.
        
        Args:
            count: Number of invalid emails to generate
            
        Returns:
            List of invalid emails
        """
        available = INVALID_BOOKING_DATA['invalid_emails']
        return [random.choice(available) for _ in range(min(count, len(available)))]
    
    @staticmethod
    def invalid_name() -> str:
        """
        Generate one invalid name.
        
        Returns:
            Invalid name (empty or too long)
        """
        return random.choice(INVALID_BOOKING_DATA['empty_names'] + 
                            INVALID_BOOKING_DATA['too_long_name'])
    
    @staticmethod
    def invalid_names(count: int = 5) -> List[str]:
        """
        Generate multiple invalid names.
        
        Args:
            count: Number of invalid names to generate
            
        Returns:
            List of invalid names
        """
        available = (INVALID_BOOKING_DATA['empty_names'] + 
                    INVALID_BOOKING_DATA['too_long_name'])
        return [random.choice(available) for _ in range(min(count, len(available)))]
    
    @staticmethod
    def negative_price() -> float:
        """
        Generate negative price for invalid data testing.
        
        Returns:
            Negative price value
        """
        return random.choice(INVALID_BOOKING_DATA['negative_prices'])
    
    @staticmethod
    def negative_prices(count: int = 3) -> List[float]:
        """
        Generate multiple negative prices.
        
        Args:
            count: Number of prices to generate
            
        Returns:
            List of negative prices
        """
        available = INVALID_BOOKING_DATA['negative_prices']
        return [random.choice(available) for _ in range(min(count, len(available)))]


class BookingDataGenerator:
    """
    Generate booking-specific test data.
    
    Provides methods to create valid and invalid booking data with realistic
    values and constraints. Used for parametrized test scenarios.
    """
    
    @staticmethod
    def valid_booking() -> Dict[str, Any]:
        """
        Generate valid booking data.
        
        Returns complete, valid booking object that should pass validation.
        Uses realistic guest names, prices, and dates.
        
        Returns:
            Dictionary with valid booking data
            
        Example:
            >>> booking = BookingDataGenerator.valid_booking()
            >>> 'firstname' in booking
            True
            >>> 0 <= booking['totalprice'] <= 999999.99
            True
        """
        checkin = datetime.now() + timedelta(days=random.randint(1, 30))
        checkout = checkin + timedelta(days=random.randint(1, 14))
        
        return {
            'firstname': random.choice(VALID_BOOKING_DATA['first_names']),
            'lastname': random.choice(VALID_BOOKING_DATA['last_names']),
            'totalprice': random.choice(VALID_BOOKING_DATA['valid_prices']),
            'depositpaid': random.choice([True, False]),
            'bookingdates': {
                'checkin': checkin.strftime('%Y-%m-%d'),
                'checkout': checkout.strftime('%Y-%m-%d'),
            },
            'additionalneeds': DataGenerator.random_string(20),
        }
    
    @staticmethod
    def valid_bookings(count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate multiple valid booking records.
        
        Args:
            count: Number of bookings to generate
            
        Returns:
            List of valid booking dictionaries
        """
        return [BookingDataGenerator.valid_booking() for _ in range(count)]
    
    @staticmethod
    def booking_with_custom_price(price: float) -> Dict[str, Any]:
        """
        Generate valid booking with specific price.
        
        Args:
            price: Price for the booking
            
        Returns:
            Valid booking data with specified price
        """
        booking = BookingDataGenerator.valid_booking()
        booking['totalprice'] = price
        return booking
    
    @staticmethod
    def booking_with_dates(checkin_days_ahead: int = 5, 
                           stay_duration: int = 3) -> Dict[str, Any]:
        """
        Generate valid booking with specific dates.
        
        Args:
            checkin_days_ahead: Days from today for check-in (default 5)
            stay_duration: How many nights to stay (default 3)
            
        Returns:
            Valid booking with specified dates
        """
        booking = BookingDataGenerator.valid_booking()
        checkin = (datetime.now() + timedelta(days=checkin_days_ahead)).strftime('%Y-%m-%d')
        checkout = (datetime.now() + 
                   timedelta(days=checkin_days_ahead + stay_duration)).strftime('%Y-%m-%d')
        
        booking['bookingdates'] = {
            'checkin': checkin,
            'checkout': checkout,
        }
        return booking
    
    @staticmethod
    def invalid_booking_empty_name() -> Dict[str, Any]:
        """
        Generate booking with empty name (invalid).
        
        Returns:
            Booking data with empty firstname
        """
        booking = BookingDataGenerator.valid_booking()
        booking['firstname'] = ''
        return booking
    
    @staticmethod
    def invalid_booking_negative_price() -> Dict[str, Any]:
        """
        Generate booking with negative price (invalid).
        
        Returns:
            Booking data with negative price
        """
        booking = BookingDataGenerator.valid_booking()
        booking['totalprice'] = DataGenerator.negative_price()
        return booking
    
    @staticmethod
    def invalid_booking_invalid_dates() -> Dict[str, Any]:
        """
        Generate booking with checkout before checkin (invalid).
        
        Returns:
            Booking data with invalid date order
        """
        booking = BookingDataGenerator.valid_booking()
        booking['bookingdates'] = {
            'checkin': '2025-12-31',
            'checkout': '2025-12-01',  # Before checkin - invalid!
        }
        return booking
    
    @staticmethod
    def invalid_booking_past_dates() -> Dict[str, Any]:
        """
        Generate booking with past dates (invalid).
        
        Returns:
            Booking data with dates in the past
        """
        booking = BookingDataGenerator.valid_booking()
        booking['bookingdates'] = INVALID_BOOKING_DATA['past_dates']
        return booking
    
    @staticmethod
    def booking_update_data() -> Dict[str, Any]:
        """
        Generate data for updating an existing booking.
        
        For PUT/PATCH requests where we only update some fields.
        
        Returns:
            Partial booking data suitable for updates
        """
        return {
            'firstname': random.choice(VALID_BOOKING_DATA['first_names']),
            'lastname': random.choice(VALID_BOOKING_DATA['last_names']),
            'totalprice': random.choice(VALID_BOOKING_DATA['valid_prices']),
            'depositpaid': random.choice([True, False]),
        }


class AuthDataGenerator:
    """
    Generate authentication test data.
    
    Provides methods to generate valid and invalid credentials for testing
    authentication flows.
    """
    
    @staticmethod
    def valid_credentials() -> Dict[str, str]:
        """
        Generate valid login credentials.
        
        Returns:
            Dictionary with 'username' and 'password'
        """
        return {
            'username': 'admin',
            'password': 'password',
        }
    
    @staticmethod
    def invalid_credentials() -> Dict[str, str]:
        """
        Generate invalid login credentials.
        
        Returns:
            Dictionary with wrong username and password
        """
        return {
            'username': DataGenerator.random_string(15),
            'password': DataGenerator.random_string(15),
        }
    
    @staticmethod
    def wrong_password() -> Dict[str, str]:
        """
        Generate credentials with correct username but wrong password.
        
        Returns:
            Dictionary with valid username but invalid password
        """
        return {
            'username': 'admin',
            'password': 'wrong_password',
        }
    
    @staticmethod
    def empty_credentials() -> Dict[str, str]:
        """
        Generate empty credentials for field validation testing.
        
        Returns:
            Dictionary with empty username and password
        """
        return {
            'username': '',
            'password': '',
        }
    
    @staticmethod
    def missing_password() -> Dict[str, str]:
        """
        Generate credentials missing password field.
        
        Returns:
            Dictionary with username but no password
        """
        return {
            'username': 'admin',
        }


class FormDataGenerator:
    """
    Generate data for web form testing.
    
    Provides methods to generate valid and invalid data for different input
    fields commonly found in web forms.
    """
    
    @staticmethod
    def valid_user_form() -> Dict[str, str]:
        """
        Generate valid user registration form data.
        
        Returns:
            Dictionary with valid form fields
        """
        return {
            'firstname': random.choice(VALID_BOOKING_DATA['first_names']),
            'lastname': random.choice(VALID_BOOKING_DATA['last_names']),
            'email': DataGenerator.random_email(),
            'phone': DataGenerator.random_phone(),
            'message': DataGenerator.random_string(50),
        }
    
    @staticmethod
    def form_with_missing_field(field_name: str) -> Dict[str, str]:
        """
        Generate form data with one required field missing.
        
        Args:
            field_name: Name of field to omit
            
        Returns:
            Form data without the specified field
        """
        form = FormDataGenerator.valid_user_form()
        if field_name in form:
            del form[field_name]
        return form
    
    @staticmethod
    def form_with_invalid_email() -> Dict[str, str]:
        """
        Generate form with invalid email address.
        
        Returns:
            Form data with invalid email
        """
        form = FormDataGenerator.valid_user_form()
        form['email'] = DataGenerator.invalid_email()
        return form
    
    @staticmethod
    def form_with_special_characters() -> Dict[str, str]:
        """
        Generate form with special characters in fields.
        
        Useful for testing form sanitization and XSS prevention.
        
        Returns:
            Form data with special characters
        """
        special_chars = '<script>alert("xss")</script>'
        form = FormDataGenerator.valid_user_form()
        form['message'] = special_chars
        return form


# ============================================================================
# EXAMPLE USAGE - Run this file to see sample data
# ============================================================================

if __name__ == '__main__':
    print("🎲 Data Generator Examples\n")
    
    print("📦 Valid Booking:")
    booking = BookingDataGenerator.valid_booking()
    print(f"  Name: {booking['firstname']} {booking['lastname']}")
    print(f"  Price: ${booking['totalprice']}")
    print(f"  Dates: {booking['bookingdates']['checkin']} → {booking['bookingdates']['checkout']}")
    
    print("\n❌ Invalid Booking (negative price):")
    invalid = BookingDataGenerator.invalid_booking_negative_price()
    print(f"  Price: ${invalid['totalprice']}")
    
    print("\n👤 Random User:")
    user = FormDataGenerator.valid_user_form()
    print(f"  Email: {user['email']}")
    print(f"  Phone: {user['phone']}")
    
    print("\n📧 Random Emails (invalid):")
    for email in DataGenerator.invalid_emails(3):
        print(f"  - {email}")
    
    print("\n✅ Data Generation Complete!")
