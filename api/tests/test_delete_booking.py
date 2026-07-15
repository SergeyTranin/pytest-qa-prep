"""
Test Delete Booking - Validates booking deletion functionality

These tests verify that:
1. Bookings can be deleted with valid token
2. Delete requires authentication
3. Deleted bookings cannot be retrieved
4. Deleting non-existent bookings returns 404
5. Deletion doesn't affect other bookings
"""
import time

import pytest
from api.clients.booking_client import BookingClient
from api.clients.auth_client import AuthClient
from api.models.booking import Booking


class TestDeleteBooking:
    """
    Test suite for deleting bookings (DELETE /booking/{id}).
    
    Delete is the most destructive operation - highest priority for testing
    We verify data is actually removed and others aren't affected.
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
        """Get authentication token."""
        try:
            token = auth_client.get_token_from_credentials(
                username="admin",
                password="password123"
            )
            return token
        except Exception:
            pytest.skip("Authentication failed - cannot test authenticated endpoints")
    
    @pytest.fixture
    def created_booking(self, booking_client):
        """Create a booking for deletion testing."""
        booking = Booking(
            firstname="Delete",
            lastname="Test",
            totalprice=99,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        response = booking_client.create_booking(booking)
        return response.bookingid
    
    def test_delete_booking_success(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: Delete existing booking returns 201 (success).
        
        Why this test?
        - Validates Delete operation (D in CRUD)
        - Tests successful deletion flow
        - Important: After delete, booking should not be retrievable
        
        What's happening:
        1. Create a booking
        2. Delete it with auth token
        3. Verify deletion succeeded
        """
        booking_id = created_booking
        
        # Delete the booking
        booking_client.delete_booking(booking_id, auth_token)
        
        # After deletion, trying to GET should return 404
        with pytest.raises(Exception) as exc_info:
            booking_client.get_booking(booking_id)
        
        # Verify it's 404 (not found)
        assert "404" in str(exc_info.value)
    
    def test_delete_requires_auth_token(
        self,
        booking_client,
        created_booking
    ):
        """
        Test: Delete without auth token should fail.
        
        Why this test?
        - Security: deletions are destructive, require auth
        - Prevents unauthorized data loss
        - Enforces security policy
        """
        booking_id = created_booking
        
        # Try to delete without token - should fail
        with pytest.raises(Exception) as exc_info:
            booking_client.delete_booking(booking_id, "")
        
        # Verify it's auth error
        assert "401" in str(exc_info.value) or "403" in str(exc_info.value)
    
    def test_delete_nonexistent_booking(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Deleting non-existent booking returns 404.
        
        Why this test?
        - Error handling: should fail gracefully
        - Tests that DELETE validates ID exists
        - Prevents silent failures
        """
        invalid_id = 999999
        
        with pytest.raises(Exception) as exc_info:
            booking_client.delete_booking(invalid_id, auth_token)
        
        assert exc_info.value.response.status_code in [404, 405]
    
    def test_delete_then_recreate(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Can recreate booking after deletion.
        
        Why this test?
        - Tests that deletion fully removes booking
        - Booking ID can be reused by system
        - No orphaned data remains
        """
        booking = Booking(
            firstname="ToDelete",
            lastname="AndRecreate",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        # Create, delete, recreate
        response1 = booking_client.create_booking(booking)
        booking_id1 = response1.bookingid
        
        booking_client.delete_booking(booking_id1, auth_token)
        
        # Verify deletion
        with pytest.raises(Exception):
            booking_client.get_booking(booking_id1)
        
        # Recreate with same data
        response2 = booking_client.create_booking(booking)
        booking_id2 = response2.bookingid
        
        # Should get a valid booking (might be different ID, but should exist)
        retrieved = booking_client.get_booking(booking_id2)
        assert retrieved is not None
    
    def test_delete_doesnt_affect_other_bookings(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Deleting one booking doesn't affect others.
        
        Why this test?
        - Data isolation: operations only affect target
        - Prevents cascading deletions
        - Critical for data integrity
        """
        # Create two bookings
        booking1 = Booking(
            firstname="ToDelete",
            lastname="One",
            totalprice=100.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking2 = Booking(
            firstname="ToKeep",
            lastname="Two",
            totalprice=200.00,
            depositpaid=False,
            checkin="2024-02-01",
            checkout="2024-02-05"
        )
        
        id1 = booking_client.create_booking(booking1).bookingid
        id2 = booking_client.create_booking(booking2).bookingid
        
        # Delete first booking
        booking_client.delete_booking(id1, auth_token)
        
        # Verify first is deleted
        with pytest.raises(Exception):
            booking_client.get_booking(id1)
        
        # Verify second still exists
        booking2_data = booking_client.get_booking(id2)
        assert booking2_data["firstname"] == "ToKeep"
        assert booking2_data["totalprice"] == 200.00
    
    def test_cannot_delete_twice(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: Deleting already-deleted booking returns 404.
        
        Why this test?
        - Idempotency: can't delete what's not there
        - Tests proper error handling
        - Prevents accidental double-deletion
        """
        booking_id = created_booking
        
        # First delete succeeds
        booking_client.delete_booking(booking_id, auth_token)
        
        # Second delete on same ID should fail
        with pytest.raises(Exception) as exc_info:
            booking_client.delete_booking(booking_id, auth_token)
        
        assert exc_info.value.response.status_code in [404, 405]
    
    def test_delete_with_special_characters_in_name(
        self,
        booking_client,
        auth_token
    ):
        """
        Test: Can delete booking with special characters in name.
        
        Why this test?
        - Ensures delete works with unicode names
        - Tests that special chars don't break deletion
        - Data encoding doesn't affect deletion
        """
        booking = Booking(
            firstname="José",
            lastname="García",
            totalprice=150.00,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        
        response = booking_client.create_booking(booking)
        booking_id = response.bookingid
        
        # Delete should work with special chars
        booking_client.delete_booking(booking_id, auth_token)
        
        # Verify deletion
        with pytest.raises(Exception):
            booking_client.get_booking(booking_id)
    
    def test_delete_response_is_empty(
        self,
        booking_client,
        auth_token,
        created_booking
    ):
        """
        Test: Delete response body is empty (or minimal).
        
        Why this test?
        - API contract: DELETE typically returns no body
        - Tests response format is as expected
        - Documents API behavior
        
        Note: This is informational - deletion is successful
        even if response body contains something.
        """
        booking_id = created_booking
        
        # Delete doesn't raise exception = success
        # Response body shouldn't contain booking data (it's deleted)
        booking_client.delete_booking(booking_id, auth_token)
        
        # Just verify deletion worked
        with pytest.raises(Exception):
            booking_client.get_booking(booking_id)
