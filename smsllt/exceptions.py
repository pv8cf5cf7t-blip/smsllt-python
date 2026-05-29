"""
Custom exceptions for the smsllt SDK.
"""


class SmslltError(Exception):
    """Base exception for all smsllt SDK errors."""

    def __init__(self, message: str = "", status_code: int = 0):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"


class AuthenticationError(SmslltError):
    """Raised when API key or login credentials are invalid (HTTP 401/403)."""


class InsufficientBalanceError(SmslltError):
    """Raised when account balance is insufficient for the requested operation."""


class NoNumberAvailableError(SmslltError):
    """Raised when no phone numbers are available for the requested service/country."""


class SmsNotReceivedError(SmslltError):
    """Raised when SMS has not been received yet (wait state)."""


class RateLimitError(SmslltError):
    """Raised when API rate limit is exceeded (HTTP 429)."""


class ServerError(SmslltError):
    """Raised when the server returns a 5xx error."""


class NetworkError(SmslltError):
    """Raised when a network/connection error occurs."""


class InvalidParameterError(SmslltError):
    """Raised when an invalid parameter is passed to the API."""


class RequestTimeoutError(SmslltError):
    """Raised when a request times out."""