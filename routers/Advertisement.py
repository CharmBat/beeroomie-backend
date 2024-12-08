from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.Advertisement import AdvertisementResponse
from schemas.Advertisement import AdPageSchema,AdPageResponseSchema
# from services.Advertisement import get_all_advertisements_service
from crud.Advertisement import AdPageCRUD
from typing import List
from db.database import get_db

router = APIRouter(
    prefix="/advertisement",
    tags=["Advertisement"]
)


# @router.get("/", response_model=AdvertisementResponse)
# async def get_all_advertisements(pagination: int = 0):#pagination is the page number(all pages has 10 advertisements)
#     return get_all_advertisements_service(pagination)

@router.post("/", response_model=AdPageResponseSchema)
def create_adpage(adpage: AdPageSchema, db: Session = Depends(get_db)):
    return AdPageCRUD.create(db, adpage)

@router.put("/{adpage_id}", response_model=AdPageResponseSchema)
def update_adpage(adpage_id: int, adpage: AdPageSchema, db: Session = Depends(get_db)):
    db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
    if not db_adpage:
        raise HTTPException(status_code=404, detail="AdPage not found")
    return AdPageCRUD.update(db, adpage_id, adpage)