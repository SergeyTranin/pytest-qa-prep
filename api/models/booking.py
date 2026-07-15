"""
Booking Models - Data structures for booking operations

These dataclasses represent the booking domain model.
They define what data a booking contains and enforce type safety.
"""
from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class Booking:
    """
    Represents a hotel booking.
    
    Think of this as a contract: any booking must have these fields.
    The API will validate them, and our code knows what to expect.
    
    Attributes:
        firstname: Guest's first name
        lastname: Guest's last name
        totalprice: Price in currency units
        depositpaid: Boolean - has deposit been paid?
        checkin: Check-in date (YYYY-MM-DD format)
        checkout: Check-out date (YYYY-MM-DD format)
        additionalneeds: Optional special requests
    """
    firstname: str
    lastname: str
    totalprice: float
    depositpaid: bool
    checkin: str  # Format: YYYY-MM-DD
    checkout: str  # Format: YYYY-MM-DD
    additionalneeds: Optional[str] = None


@dataclass
class BookingResponse:
    """
    Represents API's response when creating a booking.
    
    When we POST a booking, the API returns:
    - bookingid: The generated ID for this booking
    - booking: The full booking details (echo of what we sent)
    """
    bookingid: int
    booking: Dict[str, Any]  # Echo of booking details
