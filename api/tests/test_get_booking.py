"""
Test Get Booking - Validates booking retrieval functionality

These tests verify that:
1. Valid booking IDs return booking data
2. Invalid IDs return 404
3. Returned data has correct structure
4. Response data matches what was created
"""
import pytest
from api.clients.booking_client import BookingClient
from api.models.booking import Booking


class TestGetBooking:
    """
    Test suite for retrieving bookings (GET /booking/{id}).
    
    Test Strategy:
    - First create a booking, then retrieve it
    - This tests the full flow: Create -> Read
    - Validates data persistence
    """
    
    @pytest.fixture
    def booking_client(self):
        """Initialize booking client for tests."""
        client = BookingClient()
        yield client
        client.close()
    
    @pytest.fixture
    def created_booking(self, booking_client):
        """Create a booking and return its ID and data."""
        booking = Booking(
            firstname="Read",
            lastname="Test",
            totalprice=99.99,
            depositpaid=True,
            checkin="2024-01-15",
            checkout="2024-01-20",
            additionalneeds="Wi-Fi"
        )
        response = booking_client.create_booking(booking)
        return response.bookingid
    
    def test_get_booking_success(self, booking_client, created_booking):
        """
        Test: Retrieve existing booking returns 200 and booking data.
        
        Why this test?
        - Validates Read operation (R in CRUD)
        - Tests that created booking is retrievable
        - Checks response structure
        """
        booking_id = created_booking
        booking_data = booking_client.get_booking(booking_id)
        
        # Assertions
        assert booking_data is not None, "Should return booking data"
        assert booking_data["firstname"] == "Read"
        assert booking_data["lastname"] == "Test"
        assert booking_data["totalprice"] == 99.99
    
    def test_get_booking_returns_all_fields(self, booking_client, created_booking):
        """
        Test: Retrieved booking contains all original fields.
        
        Why this test?
        - Data completeness check
        - Ensures no fields are lost during storage
        - Validates API response format
        """
        booking_id = created_booking
        booking_data = booking_client.get_booking(booking_id)
        
        # Check that all expected fields are present
        expected_fields = [
            "firstname",
            "lastname",
            "totalprice",
            "depositpaid",
            "bookingdates",
            "additionalneeds"
        ]
        
        for field in expected_fields:
            assert field in booking_data, f"Field '{field}' should be in response"
    
    def test_get_booking_dates_structure(self, booking_client, created_booking):
        """
        Test: Booking dates are returned in correct structure.
        
        Why this test?
        - API nests dates under 'bookingdates' key
        - Need to verify this structure
        - Tests parsing of complex response format
        """
        booking_id = created_booking
        booking_data = booking_client.get_booking(booking_id)
        
        # Verify bookingdates structure
        assert "bookingdates" in booking_data
        assert "checkin" in booking_data["bookingdates"]
        assert "checkout" in booking_data["bookingdates"]
        assert booking_data["bookingdates"]["checkin"] == "2024-01-15"
        assert booking_data["bookingdates"]["checkout"] == "2024-01-20"
    
    def test_get_booking_not_found(self, booking_client):
        """
        Test: Invalid booking ID returns 404.
        
        Why this test?
        - Error handling: API should reject invalid IDs
        - Documents expected error behavior
        - Tests that 404 is raised, not silently failing
        """
        invalid_id = 999999  # Unlikely to exist
        
        with pytest.raises(Exception) as exc_info:
            booking_client.get_booking(invalid_id)
        
        # Verify it's a 404, not another error
        assert "404" in str(exc_info.value) or "Not Found" in str(exc_info.value)
    
    def test_get_booking_with_special_characters(self, booking_client):
        """
        Test: Booking with special characters in name is retrieved correctly.
        
        Why this test?
        - Unicode/special character handling
        - Tests data isn't corrupted by API
        - Validates encoding is preserved
        """
        booking = Booking(
            firstname="José",
            lastname="O'Brien",
            totalprice=200.00,
            depositpaid=True,
            checkin="2024-02-01",
            checkout="2024-02-10"
        )
        response = booking_client.create_booking(booking)
        booking_id = response.bookingid
        
        # Retrieve and verify special chars are preserved
        booking_data = booking_client.get_booking(booking_id)
        assert booking_data["firstname"] == "José"
        assert booking_data["lastname"] == "O'Brien"
    
    def test_get_booking_response_types(self, booking_client, created_booking):
        """
        Test: Response fields have correct data types.
        
        Why this test?
        - Type safety: ensures we get expected types
        - Helps identify serialization issues
        - Prevents type errors in consuming code
        """
        booking_id = created_booking
        booking_data = booking_client.get_booking(booking_id)
        
        # Type validation
        assert isinstance(booking_data["firstname"], str)
        assert isinstance(booking_data["lastname"], str)
        assert isinstance(booking_data["totalprice"], (int, float))
        assert isinstance(booking_data["depositpaid"], bool)
        assert isinstance(booking_data["bookingdates"], dict)
    
    def test_get_multiple_bookings_independently(self, booking_client):
        """
        Test: Multiple bookings can be retrieved independently.
        
        Why this test?
        - Tests isolation: one booking doesn't affect another
        - Validates API handles multiple bookings correctly
        - Documents that bookings are independent
        """
        # Create two bookings
        booking1 = Booking(
            firstname="Alice",
            lastname="First",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking2 = Booking(
            firstname="Bob",
            lastname="Second",
            totalprice=200.00,
            depositpaid=False,
            checkin="2024-02-01",
            checkout="2024-02-05"
        )
        
        response1 = booking_client.create_booking(booking1)
        response2 = booking_client.create_booking(booking2)
        
        # Retrieve both independently
        data1 = booking_client.get_booking(response1.bookingid)
        data2 = booking_client.get_booking(response2.bookingid)
        
        # Verify they're different
        assert data1["firstname"] == "Alice"
        assert data2["firstname"] == "Bob"
        assert data1["totalprice"] == 100.00
        assert data2["totalprice"] == 200.00
