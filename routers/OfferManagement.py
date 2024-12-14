from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.OfferManagement import OfferResponse
from services.OfferManagement import OfferService
from typing import List
from db.database import get_db

router = APIRouter(prefix="/offers",
    tags=["Offers"])

@router.post("/", response_model=OfferResponse)
async def create_offer(adpageid: int, description:str, token: str, db: Session =Depends(get_db)):
    return OfferService.create_offer_service(adpageid, description, db, token)

