from fastapi import HTTPException


class CacheError(HTTPException):
    """Исключение для обработки ошибок кэширования."""

    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)
