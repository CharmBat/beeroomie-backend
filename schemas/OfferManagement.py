from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class Offer(BaseModel):
    offer_id: int
    send_message: str
    offerer_name: str
    contact_info: str
    other_user_id: int
    ppurl: str
    
    
class OfferResponse(BaseModel):
    user_message: str
    error_status: int
    system_message: str
    offers: Optional[List[Offer]] = None
