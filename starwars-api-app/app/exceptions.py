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


