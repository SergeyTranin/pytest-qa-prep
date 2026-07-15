"""
Booking Client - Handles all booking-related API endpoints

This client manages CRUD operations (Create, Read, Update, Delete) for bookings.
It's the main interface for interacting with booking resources.
"""
from api.clients.base_client import BaseClient
from api.models.booking import Booking, BookingResponse
from typing import Optional, Dict, Any
from datetime import datetime
import time


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

    def wait_for_booking(self, booking_id: int, retries=5, delay=1):
        """
        Wait until booking becomes available.
        Handles eventual consistency of Restful Booker API.
        """
        for _ in range(retries):
            response = self.get(f"{self.BOOKINGS_ENDPOINT}/{booking_id}")

            if response.status_code == 200:
                return True

            time.sleep(delay)

        return False

    def _validate_booking(self, booking: Booking):
        if not booking.firstname:
            raise ValueError("Firstname cannot be empty")

        if not booking.lastname:
            raise ValueError("Lastname cannot be empty")

        if booking.totalprice < 0:
            raise ValueError("Total price cannot be negative")

        checkin_date = datetime.strptime(
            booking.checkin,
            "%Y-%m-%d"
        )

        checkout_date = datetime.strptime(
            booking.checkout,
            "%Y-%m-%d"
        )

        if checkout_date <= checkin_date:
            raise ValueError(
                "Checkout must be after checkin"
            )
    
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
        self._validate_booking(booking)

        headers = {}
        if auth_token:
            headers["Cookie"] = f"token={auth_token}"
        
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
        - Requires token cookie authentication
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
        headers = {"Cookie": f"token={auth_token}"}
        
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
        - Requires token cookie authentication
        - Returns 201 on success (no body)
        
        Args:
            booking_id: The booking ID to delete
            auth_token: Required authentication token
        
        Raises:
            requests.RequestException: On network errors
        """
        self.wait_for_booking(booking_id)

        endpoint = f"{self.BOOKINGS_ENDPOINT}/{booking_id}"
        headers = {"Cookie": f"token={auth_token}"}
        
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
