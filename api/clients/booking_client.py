"""
Booking Client - Handles all booking-related API endpoints

This client manages CRUD operations (Create, Read, Update, Delete) for bookings.
It's the main interface for interacting with booking resources.
"""
from api.clients.base_client import BaseClient
from api.models.booking import Booking, BookingResponse
from typing import Optional, Dict, Any
import requests


class BookingClient(BaseClient):
    """
    Booking client for managing hotel bookings via API.
    
    This demonstrates the Client-Model pattern:
    - Client: Handles HTTP communication
    - Model: Represents data structure
    
    Benefits:
    - Type-safe: Models validate data structure
    - Testable: Can mock responses easily
    - Maintainable: Changes to API structure only need model updates
    """
    
    BOOKINGS_ENDPOINT = "/booking"
    
    def create_booking(
        self,
        booking: Booking,
        auth_token: Optional[str] = None
    ) -> BookingResponse:
        """
        Create a new booking.
        
        API behavior:
        - POST to /booking
        - Send booking data in body
        - Returns created booking with ID
        
        Args:
            booking: Booking object with details
            auth_token: Optional authentication token (some APIs require this)
        
        Returns:
            BookingResponse with booking ID and details
        
        Raises:
            requests.RequestException: On network errors
            ValueError: If response format is invalid
        """
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        payload = {
            "firstname": booking.firstname,
            "lastname": booking.lastname,
            "totalprice": booking.totalprice,
            "depositpaid": booking.depositpaid,
            "bookingdates": {
                "checkin": booking.checkin,
                "checkout": booking.checkout
            }
        }
        
        if booking.additionalneeds:
            payload["additionalneeds"] = booking.additionalneeds
        
        response = self.post(self.BOOKINGS_ENDPOINT, data=payload, headers=headers)
        response.raise_for_status()
        
        try:
            data = response.json()
            return BookingResponse(
                bookingid=data.get("bookingid"),
                booking=data.get("booking")
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid booking response format: {str(e)}")
    
    def get_booking(self, booking_id: int) -> Dict[str, Any]:
        """
        Retrieve a specific booking by ID.
        
        API behavior:
        - GET to /booking/{id}
        - Returns booking details
        
        Args:
            booking_id: The booking ID to retrieve
        
        Returns:
            Dictionary with booking details
        
        Raises:
            requests.RequestException: On network errors (404 if not found)
        """
        endpoint = f"{self.BOOKINGS_ENDPOINT}/{booking_id}"
        response = self.get(endpoint)
        response.raise_for_status()
        
        return response.json()
    
    def update_booking(
        self,
        booking_id: int,
        booking: Booking,
        auth_token: str
    ) -> Dict[str, Any]:
        """
        Update an existing booking.
        
        API behavior:
        - PUT to /booking/{id}
        - Requires authentication token
        - Returns updated booking
        
        Args:
            booking_id: The booking ID to update
            booking: Updated booking object
            auth_token: Required authentication token
        
        Returns:
            Dictionary with updated booking details
        
        Raises:
            requests.RequestException: On network errors
        """
        endpoint = f"{self.BOOKINGS_ENDPOINT}/{booking_id}"
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        payload = {
            "firstname": booking.firstname,
            "lastname": booking.lastname,
            "totalprice": booking.totalprice,
            "depositpaid": booking.depositpaid,
            "bookingdates": {
                "checkin": booking.checkin,
                "checkout": booking.checkout
            }
        }
        
        if booking.additionalneeds:
            payload["additionalneeds"] = booking.additionalneeds
        
        response = self.put(endpoint, data=payload, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def delete_booking(self, booking_id: int, auth_token: str) -> None:
        """
        Delete a booking.
        
        API behavior:
        - DELETE to /booking/{id}
        - Requires authentication token
        - Returns 201 on success (no body)
        
        Args:
            booking_id: The booking ID to delete
            auth_token: Required authentication token
        
        Raises:
            requests.RequestException: On network errors
        """
        endpoint = f"{self.BOOKINGS_ENDPOINT}/{booking_id}"
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = self.delete(endpoint, headers=headers)
        response.raise_for_status()
    
    def get_booking_ids(self) -> list:
        """
        Get list of all booking IDs.
        
        API behavior:
        - GET to /booking
        - Returns array of booking ID objects
        
        Returns:
            List of booking ID dictionaries
        """
        response = self.get(self.BOOKINGS_ENDPOINT)
        response.raise_for_status()
        
        return response.json()
