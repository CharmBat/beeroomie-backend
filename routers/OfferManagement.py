from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.OfferManagement import OfferResponse
from services.OfferManagement import OfferService
from typing import List
from db.database import get_db
from services.Authentication import AuthenticationService
from schemas.Authentication import TokenData
from crud.OfferManagement import OfferCRUD
router = APIRouter(prefix="/offers",
    tags=["Offers"])

@router.post("/", response_model=OfferResponse)
async def create_offer(adpageid: int, description:str,db: Session =Depends(get_db),current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return OfferService.create_offer_service(adpageid, description, db, current_user.userid)
    else:
        return current_user

@router.delete("/{offerid}", response_model=OfferResponse)
async def delete_offer(offerid: int, db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        if current_user.userid == OfferCRUD.get_userid_by_offer(db, offerid):
            return OfferService.delete_offer_service(offerid, db)
    else:
        return current_user

@router.get("/", response_model=OfferResponse)
async def get_offers(db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return OfferService.get_offers_service(db=db, user_id=current_user.userid)
    else:
        return current_user
