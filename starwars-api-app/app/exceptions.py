from functools import wraps

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, SQLAlchemyError


class BaseError(HTTPException):
    """Base class for all custom API errors"""

    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str | None = None):
        super().__init__(status_code=self.status, detail=detail or self.__doc__)


class SwapiUnavailableError(BaseError):
    """SWAPI service is unavailable"""

    status = status.HTTP_503_SERVICE_UNAVAILABLE


class NotFoundError(BaseError):
    """Requested resource not found"""

    status = status.HTTP_404_NOT_FOUND


class DatabaseError(BaseError):
    """Database operation failed"""

    status = status.HTTP_503_SERVICE_UNAVAILABLE


def add_exception_handlers(app: FastAPI):
    """Register exception handlers for all subclasses of BaseError."""
    for exception_class in BaseError.__subclasses__():
        app.add_exception_handler(
            exception_class,
            _get_handler(
                status=exception_class.status,
                detail=exception_class.__doc__,
            ),
        )


def _get_handler(status: int, detail: str):
    """Return a JSON error handler for the given status and detail."""

    async def handler(request: Request, exc: BaseError):
        """Handle a raised BaseError and return a JSON error response."""
        return JSONResponse(
            status_code=status,
            content={"error": detail, "exception": str(exc)},
        )

    return handler
