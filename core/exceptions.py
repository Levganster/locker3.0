"""
Define your global custom exceptions in this file
"""

from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self, detail=None) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        if detail is None:
            detail  = "Bad Request"
        super().__init__(status_code, detail)


class NotFoundException(HTTPException):
    def __init__(self, detail=None) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        if detail is None:
            detail = "The requested resource was not found"
        super().__init__(status_code, detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail=None) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        if detail is None:
            detail = "You are not authorized to access this resource"
        super().__init__(status_code, detail)


class ConflictException(HTTPException):
    def __init__(self, detail=None) -> None:
        status_code = status.HTTP_409_CONFLICT
        if detail is None:
            detail = "Conflict: The resource already exists."
        super().__init__(status_code, detail)

