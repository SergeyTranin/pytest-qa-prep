"""
Auth Client - Handles authentication/authorization endpoints

This client manages user authentication operations like login.
It inherits from BaseClient to reuse HTTP methods.
"""
from api.clients.base_client import BaseClient
from api.models.auth import AuthCredentials, AuthResponse
from typing import Optional
import requests


class AuthClient(BaseClient):
    """
    Authentication client for API login operations.
    
    Inheritance: This class extends BaseClient, demonstrating OOP principles.
    We inherit the HTTP methods (get, post, put, delete) instead of rewriting them.
    
    Why separation? Auth might need special handling (retry logic, token refresh, etc.)
    that booking operations don't need. Separation allows for flexibility.
    """
    
    AUTH_ENDPOINT = "/auth"
    
    def login(self, credentials: AuthCredentials) -> AuthResponse:
        """
        Authenticate user and get token.
        
        The Restful Booker API expects:
        - POST request
        - Username and password in body
        - Returns a token for subsequent authenticated requests
        
        Args:
            credentials: AuthCredentials object with username and password
        
        Returns:
            AuthResponse with token
        
        Raises:
            requests.RequestException: On network errors
            ValueError: If response format is invalid
        """
        payload = {
            "username": credentials.username,
            "password": credentials.password
        }
        
        response = self.post(self.AUTH_ENDPOINT, data=payload)
        
        # Check for HTTP errors (401, 500, etc.)
        response.raise_for_status()
        
        # Parse and validate response
        try:
            data = response.json()
            return AuthResponse(token=data.get("token"))
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid auth response format: {str(e)}")
    
    def get_token_from_credentials(self, username: str, password: str) -> str:
        """
        Convenience method - get token string directly.
        
        Args:
            username: User's username
            password: User's password
        
        Returns:
            Auth token string
        """
        credentials = AuthCredentials(username=username, password=password)
        auth_response = self.login(credentials)
        return auth_response.token
