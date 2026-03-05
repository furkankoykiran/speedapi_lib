"""Custom exception hierarchy for the Speed API SDK."""

from __future__ import annotations

from typing import Optional


class SpeedAPIError(Exception):
    """Base class for all Speed API errors.

    Attributes:
        message: Human-readable description of the error.
        status_code: HTTP status code, if available.
        response_body: Raw response body from the API, if available.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"status_code={self.status_code!r})"
        )


class AuthenticationError(SpeedAPIError):
    """Raised when the API key is invalid or missing (HTTP 401).

    Example:
        >>> raise AuthenticationError("Invalid API key provided.")
        AuthenticationError: Invalid API key provided.
    """


class PermissionDeniedError(SpeedAPIError):
    """Raised when the API key lacks the required permissions (HTTP 403)."""


class NotFoundError(SpeedAPIError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(SpeedAPIError):
    """Raised when the API rate limit has been exceeded (HTTP 429).

    Back off before retrying the request.
    """


class APIStatusError(SpeedAPIError):
    """Raised for unexpected 4xx / 5xx responses not covered by a specific subclass."""


class APIConnectionError(SpeedAPIError):
    """Raised for network-level failures (timeout, DNS error, connection refused).

    Unlike :class:`APIStatusError`, this exception carries no HTTP status code
    because the request never reached the server (or no response was received).
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=None, response_body=None)
