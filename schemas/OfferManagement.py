from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from models.OfferManagement import OfferModel

class OfferResponse(BaseModel):
    offer_list: Optional[List[OfferModel]]
    user_message: str
    error_status: int
    system_message: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

