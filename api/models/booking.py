from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class Booking:
    """
    Represents a hotel booking.
    """

    firstname: str
    lastname: str
    totalprice: float
    depositpaid: bool
    checkin: str
    checkout: str
    additionalneeds: Optional[str] = None


@dataclass
class BookingResponse:
    """
    Represents response returned after creating a booking.
    """

    bookingid: int
    booking: Dict[str, Any]