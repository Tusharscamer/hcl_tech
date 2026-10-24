from typing import Optional, Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None
    error: Optional[str] = None
    trace_id: Optional[str] = None
