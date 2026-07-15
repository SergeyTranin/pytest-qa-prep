"""
Base HTTP Client - Foundation for all API interactions

This class handles core HTTP operations (GET, POST, PUT, DELETE) with built-in
error handling, response logging, and timeout management. It acts as a wrapper
around the requests library, standardizing how we communicate with APIs.
"""
import requests
from typing import Dict, Any, Optional
from config.settings import settings


class BaseClient:
    """
    Base client for making HTTP requests with centralized configuration.
    
    Design Pattern: This is a "Wrapper" pattern - we wrap the requests library
    to standardize all API calls across the project.
    
    Benefits:
    - Single source of truth for base URL and timeouts
    - Consistent error handling across all requests
    - Easy to mock/test
    - Simplifies adding headers, auth, or middleware later
    """
    
    def __init__(self, base_url: str = settings.api_base_url):
        """
        Initialize the base client.
        
        Args:
            base_url: The API base URL (defaults from settings)
        """
        self.base_url = base_url
        self.timeout = settings.request_timeout
        self.session = requests.Session()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request - Internal method for all HTTP operations.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/bookings")
            data: Request body (for POST/PUT)
            headers: Custom headers
            **kwargs: Additional arguments passed to requests
        
        Returns:
            Response object from requests library
        
        Raises:
            requests.RequestException: On network errors
        """
        url = f"{self.base_url}{endpoint}"
        
        # Default headers
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            return response
        except requests.RequestException as e:
            print(f"Request failed: {method} {url} - {str(e)}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request"""
        return self._make_request("GET", endpoint, **kwargs)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """POST request"""
        return self._make_request("POST", endpoint, data=data, **kwargs)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """PUT request"""
        return self._make_request("PUT", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        return self._make_request("DELETE", endpoint, **kwargs)
    
    def close(self):
        """Close the session"""
        self.session.close()
