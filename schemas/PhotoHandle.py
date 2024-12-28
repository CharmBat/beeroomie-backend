from pydantic import BaseModel
from typing import Optional


class PhotoHandleResponse(BaseModel):
    photoUrl: Optional[str] = None
    user_message: str
    error_status:int
    system_message: str    
