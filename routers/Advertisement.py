from fastapi import APIRouter, Depends
from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageFilterSchema
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

@router.get("/", response_model=AdPageResponse)
async def get_advertisements(filters: AdPageFilterSchema = Depends(), pagination: int = 0, db: Session = Depends(get_db)
):
    if filters.dict(exclude_unset=True):  #If there is a filter
        return AdvertisementService.get_filtered_advertisements_service(filters, db, pagination)
    
    else:  #If there is no filter
        return AdvertisementService.get_all_advertisements_service(pagination, db)


@router.post("/", response_model=AdPageResponse)
async def create_adpage(adpage: AdPageRequest, db: Session =Depends(get_db)):
    return AdvertisementService.create_adpage_service(adpage,db)


@router.put("/{adpage_id}", response_model=AdPageResponse)
async def update_adpage(adpage_id: int, adpage: AdPageRequest, db: Session =Depends(get_db)):
    return AdvertisementService.update_adpage_service(adpage_id, adpage,db)




