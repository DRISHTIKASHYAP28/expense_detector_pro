"""
utils/exceptions.py
-------------------
Centralised domain exceptions mapped to HTTP status codes.
"""


class AppException(Exception):
    """Base application exception."""

    status_code = 500

    def __init__(
        self, message: str, status_code: int = None, payload: dict = None
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        """Serialise exception details."""
        result = dict(self.payload or ())
        result["error"] = self.message
        return result


class ValidationError(AppException):
    """Exception for request parameter validation failures."""

    status_code = 400


class AuthenticationError(AppException):
    """Exception for authentication failures."""

    status_code = 401


class ForbiddenError(AppException):
    """Exception for unauthorised actions on resources."""

    status_code = 403


class ResourceNotFoundError(AppException):
    """Exception when a requested database resource does not exist."""

    status_code = 404
