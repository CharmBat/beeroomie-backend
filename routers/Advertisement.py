from fastapi import APIRouter, Depends
from schemas.Advertisement import AdPageSchema, AdPageResponse
from services.Advertisement import AdvertisementService
from db.database import get_db
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/advertisement",
    tags=["Advertisement"]
)

# @router.get("/", response_model=AdPageResponse)
# async def get_all_advertisements(pagination: int = 0, db: Session =Depends(get_db)):  # pagination is the page number (all pages have 10 advertisements)
#     return AdvertisementService.get_all_advertisements_service(pagination,db)

@router.post("/", response_model=AdPageResponse)
async def create_adpage(adpage: AdPageSchema, db: Session =Depends(get_db)):
    return AdvertisementService.create_adpage_service(adpage,db)


@router.put("/{adpage_id}", response_model=AdPageResponse)
async def update_adpage(adpage_id: int, adpage: AdPageSchema, db: Session =Depends(get_db)):
    return AdvertisementService.update_adpage_service(adpage_id, adpage,db)

