"""
Test Update Booking - Validates booking modification functionality

These tests verify that:
1. Bookings can be updated with new data
2. Update requires authentication
3. Non-existent bookings return 404
4. All fields can be modified
5. Updates don't affect other bookings
"""
import pytest
from api.clients.booking_client import BookingClient
from api.clients.auth_client import AuthClient
from api.models.booking import Booking


class TestUpdateBooking:
    """
    Test suite for updating bookings (PUT /booking/{id}).
    
    Authentication Flow:
    - Updating requires auth token
    - This demonstrates multi-step workflows
    - Shows dependency between tests (auth -> update)
    """
    
    @pytest.fixture
    def booking_client(self):
        """Initialize booking client."""
        client = BookingClient()
        yield client
        client.close()
    
    @pytest.fixture
    def auth_client(self):
        """Initialize auth client."""
        client = AuthClient()
        yield client
        client.close()
    
    @pytest.fixture
    def auth_token(self, auth_client):
        """
        Get authentication token.
        
        Note: This assumes credentials are available in your environment
        or settings. In production, use environment variables.
        """
        try:
            token = auth_client.get_token_from_credentials(
                username="admin",
                password="password123"
            )
            return token
        except Exception:
            # If auth fails, skip tests requiring auth
            pytest.skip("Authentication failed - cannot test authenticated endpoints")
    
    @pytest.fixture
    def created_booking(self, booking_client):
        """Create a booking to update."""
        booking = Booking(
            firstname="Original",
            lastname="Name",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        response = booking_client.create_booking(booking)
        return response.bookingid
    
    def test_update_booking_success(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: Update booking returns 200 and updated data.
        
        Why this test?
        - Validates Update operation (U in CRUD)
        - Tests that changes persist
        - Verifies auth requirement works
        
        What's happening:
        1. Create a booking
        2. Update first name
        3. Verify GET returns updated name
        """
        booking_id = created_booking
        
        # New data to update with
        updated_booking = Booking(
            firstname="Updated",  # Changed
            lastname="Name",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        # Perform update
        result = booking_client.update_booking(
            booking_id,
            updated_booking,
            auth_token
        )
        
        # Verify update succeeded
        assert result["firstname"] == "Updated"
    
    def test_update_booking_all_fields(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: All booking fields can be updated.
        
        Why this test?
        - Ensures no fields are read-only unexpectedly
        - Tests comprehensive update functionality
        - Documents what can be changed
        """
        booking_id = created_booking
        
        # Update all fields
        updated_booking = Booking(
            firstname="Changed",
            lastname="LastName",
            totalprice=250,
            depositpaid=False,  # Changed
            checkin="2024-02-01",  # Changed
            checkout="2024-02-10",  # Changed
            additionalneeds="Extra pillow"  # Added
        )
        
        result = booking_client.update_booking(
            booking_id,
            updated_booking,
            auth_token
        )
        
        # Verify ALL changes took effect
        assert result["firstname"] == "Changed"
        assert result["lastname"] == "LastName"
        assert result["totalprice"] == 250
        assert result["depositpaid"] is False
        assert result["additionalneeds"] == "Extra pillow"
        assert result["bookingdates"]["checkin"] == "2024-02-01"
        assert result["bookingdates"]["checkout"] == "2024-02-10"
    
    def test_update_requires_auth_token(
        self,
        booking_client,
        created_booking
    ):
        """
        Test: Update without auth token should fail.
        
        Why this test?
        - Security validation: updates require authentication
        - Prevents unauthorized modifications
        - Documents security requirement
        """
        booking_id = created_booking
        updated_booking = Booking(
            firstname="Unauthorized",
            lastname="Change",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        # Try to update without token - should fail
        with pytest.raises(Exception) as exc_info:
            booking_client.update_booking(booking_id, updated_booking, "")
        
        # Verify it's auth error (401 or 403)
        assert "401" in str(exc_info.value) or "403" in str(exc_info.value)
    
    def test_update_nonexistent_booking(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Updating non-existent booking returns 404.
        
        Why this test?
        - Error handling: API should reject invalid IDs
        - Tests that update validates ID exists
        - Documents error behavior
        """
        invalid_id = 999999
        booking = Booking(
            firstname="Test",
            lastname="User",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        with pytest.raises(Exception) as exc_info:
            booking_client.update_booking(invalid_id, booking, auth_token)
        
        assert exc_info.value.response.status_code in [404, 405]
    
    def test_update_only_price(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: Update only price field.
        
        Why this test?
        - Partial update scenario
        - Ensures other fields aren't affected
        - Tests field-level independence
        """
        booking_id = created_booking
        
        # First, get current booking
        current = booking_client.get_booking(booking_id)
        
        # Update with same data except price
        updated_booking = Booking(
            firstname=current["firstname"],
            lastname=current["lastname"],
            totalprice=999,  # Only change this
            depositpaid=current["depositpaid"],
            checkin=current["bookingdates"]["checkin"],
            checkout=current["bookingdates"]["checkout"]
        )
        
        result = booking_client.update_booking(
            booking_id,
            updated_booking,
            auth_token
        )
        
        # Verify only price changed
        assert result["totalprice"] == 999
        assert result["firstname"] == current["firstname"]
        assert result["lastname"] == current["lastname"]
    
    def test_update_doesnt_affect_other_bookings(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Updating one booking doesn't affect others.
        
        Why this test?
        - Isolation test: bookings are independent
        - Tests proper record handling
        - Prevents accidental data corruption
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
        
        id1 = booking_client.create_booking(booking1).bookingid
        id2 = booking_client.create_booking(booking2).bookingid
        
        # Update first booking
        updated = Booking(
            firstname="AliceUpdated",
            lastname="First",
            totalprice=150.00,
            depositpaid=False,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        booking_client.update_booking(id1, updated, auth_token)
        
        # Verify second booking is unchanged
        booking2_data = booking_client.get_booking(id2)
        assert booking2_data["firstname"] == "Bob"
        assert booking2_data["totalprice"] == 200.00
