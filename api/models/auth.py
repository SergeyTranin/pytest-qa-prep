"""
Auth Models - Data structures for authentication

These are Pydantic-like dataclasses that define the shape of auth data.
They serve as contracts between tests and the API.
"""
from dataclasses import dataclass


@dataclass
class AuthCredentials:
    """
    Represents authentication credentials.
    
    Dataclasses: Python's built-in way to create data classes automatically.
    Benefits: Type hints, automatic __init__, __repr__, __eq__
    """
    username: str
    password: str


@dataclass
class AuthResponse:
    """
    Represents API's auth response.
    
    This models what the Restful Booker API returns when you login.
    Having a model lets tests be explicit about what they expect.
    """
    token: str
