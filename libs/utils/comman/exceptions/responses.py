from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool
    code: str
    message: str
    details: dict[str, Any] | str | list[Any] | None = None


class SuccessResponse(BaseModel):
    success: bool
    code: str
    message: dict[str, Any] | str | list[Any] | None = None
