"""
Test Create Booking - Validates booking creation functionality

These tests verify that:
1. Valid bookings are created successfully
2. Invalid data is rejected
3. Response contains expected fields
4. Status codes are correct
"""
import pytest
from api.clients.booking_client import BookingClient
from api.models.booking import Booking


class TestCreateBooking:
    """
    Test suite for booking creation (POST /booking).
    
    Test Class Pattern:
    - Groups related tests together
    - setup_method() runs before EACH test (fresh state)
    - Easier to read than individual test functions
    """
    
    @pytest.fixture
    def booking_client(self):
        """
        Fixture: Setup that runs before each test.
        
        Why fixtures?
        - Eliminates duplication
        - Manages cleanup (close session after test)
        - Makes tests readable
        """
        client = BookingClient()
        yield client
        client.close()
    
    @pytest.fixture
    def valid_booking(self):
        """Valid booking data for happy path tests."""
        return Booking(
            firstname="John",
            lastname="Doe",
            totalprice=100.50,
            depositpaid=True,
            checkin="2024-01-15",
            checkout="2024-01-20",
            additionalneeds="Late checkout"
        )
    
    def test_create_booking_success(self, booking_client, valid_booking):
        """
        Test: Create booking returns 200 and booking ID.
        
        Why this test?
        - Happy path: Most common scenario users will experience
        - Validates the basic flow works
        - Tests integration between Client and API
        
        What we're checking:
        1. Response status is successful (200)
        2. Response has a bookingid
        3. Response echoes back our booking data
        """
        response = booking_client.create_booking(valid_booking)
        
        # Assertions verify expected behavior
        assert response.bookingid is not None, "Booking ID should be returned"
        assert isinstance(response.bookingid, int), "Booking ID should be integer"
        assert response.booking is not None, "Booking details should be returned"
    
    def test_create_booking_with_all_fields(self, booking_client):
        """
        Test: Booking creation preserves all provided fields.
        
        Why this test?
        - Ensures no data is lost in transmission
        - Validates our model matches API expectations
        """
        booking = Booking(
            firstname="Jane",
            lastname="Smith",
            totalprice=250.00,
            depositpaid=False,
            checkin="2024-02-01",
            checkout="2024-02-05",
            additionalneeds="Extra bed"
        )
        
        response = booking_client.create_booking(booking)
        
        # Verify all fields are in response
        assert response.booking["firstname"] == "Jane"
        assert response.booking["lastname"] == "Smith"
        assert response.booking["totalprice"] == 250.00
        assert response.booking["depositpaid"] is False
        assert response.booking["additionalneeds"] == "Extra bed"
    
    def test_create_booking_without_additional_needs(self, booking_client):
        """
        Test: Booking works without optional additionalneeds field.
        
        Why this test?
        - Additionalneeds is optional
        - Should still create booking successfully
        - Tests default values work correctly
        """
        booking = Booking(
            firstname="Bob",
            lastname="Johnson",
            totalprice=150.00,
            depositpaid=True,
            checkin="2024-03-10",
            checkout="2024-03-12"
        )
        
        response = booking_client.create_booking(booking)
        
        assert response.bookingid is not None
    
    def test_create_booking_invalid_dates_order(self, booking_client):
        """
        Test: Checkout date before checkin should fail.
        
        Why this test?
        - Business logic validation: checkout must be after checkin
        - API should reject logically invalid data
        - Tests error handling
        """
        invalid_booking = Booking(
            firstname="Test",
            lastname="User",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-20",  # Checkout date
            checkout="2024-01-15"  # Checkin date (WRONG ORDER)
        )
        
        # This should raise an exception
        with pytest.raises(Exception):
            booking_client.create_booking(invalid_booking)
    
    def test_create_booking_zero_price(self, booking_client):
        """
        Test: Zero price booking should be accepted.
        
        Why this test?
        - Boundary condition: can price be 0?
        - Some APIs have business rules about this
        - Documents behavior for review
        """
        booking = Booking(
            firstname="Free",
            lastname="Tier",
            totalprice=0.0,
            depositpaid=False,
            checkin="2024-01-01",
            checkout="2024-01-02"
        )
        
        response = booking_client.create_booking(booking)
        assert response.bookingid is not None
    
    def test_create_booking_negative_price(self, booking_client):
        """
        Test: Negative price should be rejected.
        
        Why this test?
        - Business rule: price cannot be negative
        - API should validate this
        - Tests input validation
        """
        booking = Booking(
            firstname="Negative",
            lastname="Price",
            totalprice=-100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-02"
        )
        
        with pytest.raises(Exception):
            booking_client.create_booking(booking)
    
    def test_create_booking_empty_name(self, booking_client):
        """
        Test: Empty firstname should be rejected.
        
        Why this test?
        - Required field validation
        - API should enforce data quality
        - Tests field validation
        """
        booking = Booking(
            firstname="",  # Empty
            lastname="Doe",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-02"
        )
        
        with pytest.raises(Exception):
            booking_client.create_booking(booking)
