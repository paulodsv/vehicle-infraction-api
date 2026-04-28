from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

def success_response(data: T, message: str = "OK") -> APIResponse[T]:
    return APIResponse(success=True, message=message, data=data)

def error_response(message: str) -> APIResponse[None]:
    return APIResponse(success=False, message=message, data=None)