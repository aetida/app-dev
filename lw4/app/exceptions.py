from litestar import status_codes
from litestar.exceptions import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status_codes.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ConflictException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status_codes.HTTP_409_CONFLICT,
            detail=detail,
        )
