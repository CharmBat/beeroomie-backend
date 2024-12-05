from fastapi import Depends,APIRouter
from schemas.Advertisement import AdvertisementResponse
from services.Advertisement import get_all_advertisements_service
from typing import List

router = APIRouter(tags=["Advertisement"])

@router.get("/advertisement", response_model=AdvertisementResponse)
async def get_all_advertisements(pagination: int = 0):#pagination is the page number(all pages has 10 advertisements)
    return get_all_advertisements_service(pagination)