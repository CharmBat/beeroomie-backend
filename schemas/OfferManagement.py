from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class Offer(BaseModel):
    description: str
class OfferResponse(BaseModel):
    user_message: str
    error_status: int
    system_message: str

