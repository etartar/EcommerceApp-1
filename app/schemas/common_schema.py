from pydantic import BaseModel
from typing import Any, Optional, List

class SuccessResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool
    message: str
    errors: Optional[List[str]] = None