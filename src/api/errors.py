import logging

from fastapi import HTTPException, Request, status
from fastapi.responses import ORJSONResponse

from src.api.helpers import get_allowed_methods
from src.internal.dependency import get_logger


class APIError(HTTPException):
    """Base API error that returns enveloped json response, primarily used to create other error classes for 4** errors.
    This is less intended to be used as practical code and more of a demonstration of creating custom errors and responses, and to integrate that with logging."""

    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.message = message


class NotFoundError(APIError):
    """custom 404 wrapper, used to throw an error when a requested resource was not found"""

    def __init__(self, message: str = "the requested resource could not be found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class MethodNotAllowedError(APIError):
    """custom 405 wrapper, used when the requested method is disallowed"""

    def __init__(self, allowed_methods: list[str]):
        # Join the methods (e.g., "GET, POST, OPTIONS")
        methods_str = ", ".join(allowed_methods)
        message = (
            f"the requested method is not supported. Supported methods: {methods_str}"
        )
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, message=message
        )


class ServerError(Exception):
    """500 unknown server error wrapper"""

    def __init__(
        self,
        message: str = "the server encountered a problem and could not process your request",
    ):
        self.message = message
        super().__init__(self.message)


def log_error(request: Request, error: Exception, logger: logging.Logger):
    """log error with request details"""
    logging.error(
        str(error), extra={"method": request.method, "uri": str(request.url.path)}
    )


def error_response(
    status_code: int, message: str | dict, headers: dict | None
) -> ORJSONResponse:
    """Standardized JSON envelope."""
    return ORJSONResponse(
        status_code=status_code, content={"error": message}, headers=headers
    )


async def http_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    """
    Equivalent to the book's clientError (and manual server errors).
    Catches explicit raise HTTPException(...) calls and framework 404/405s.
    """
    # assume an HTTPException
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "Internal Server Error")

    # mirrors pattern for malformed json input
    # however fastapi and pydantic handle this for us
    if "decode error" in str(detail).lower():
        detail = "the request body contains badly-formd JSON"
        status_code = 400

    if status_code == 405:
        allowed = get_allowed_methods(request=request)
        detail = f"the {request.method} method is not supported for this resource. Supported: {', '.join(allowed)}"

        headers = {"Allow": ", ".join(allowed)}
        return error_response(status_code=status_code, message=detail, headers=headers)

    logger = get_logger()
    logger.error(f"Unhandled Exception: {exc}, request @ {request.url.path}")
    return error_response(status_code, detail, None)


async def general_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    """
    Equivalent to the book's serverError helper with panic recovery, it also handles the case handled by the recoverPanic middleware.
    Catches unhandled exceptions (e.g., ZeroDivisionError, KeyErrors).
    """
    logger = get_logger()
    logger.error(
        f"Unhandled Exception; server error: {exc}",
        extra={"request_method": request.method, "request_url": request.url},
        exc_info=True,
    )

    # mirrors recoverPanic handler
    headers = {"Connection": "close"}

    return error_response(500, "The server could not process your request", headers)
