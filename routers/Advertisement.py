from fastapi import APIRouter, Depends
from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageFilterSchema, AdPageRequest, AdPageResponse, AdPageFilterSchema, UtilityListResponse, DepartmentListResponse, DistrictListResponse, NeighborhoodListResponse, NumberOfRoomListResponse
from services.Advertisement import AdvertisementService
from db.database import get_db
from sqlalchemy.orm import Session
from schemas.Authentication import TokenData
from services.Authentication import AuthenticationService
from crud.Advertisement import AdPageCRUD
router = APIRouter(
    prefix="/advertisement",
    tags=["Advertisement"]
)

@router.get("/rooms", response_model=NumberOfRoomListResponse)
async def get_all_rooms(
    db: Session = Depends(get_db),
    current_user=Depends(AuthenticationService.get_current_user)
):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_all_rooms_service(db)
    else:
        return current_user

@router.get("/neighborhood/{district_id}", response_model=NeighborhoodListResponse)
async def get_neighborhoods_by_district(
    district_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthenticationService.get_current_user)
):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_neighborhoods_by_district_service(db, district_id)
    else:
        return current_user

@router.get("/district", response_model=DistrictListResponse)
async def get_advertisement_district(
    db: Session = Depends(get_db),
    current_user=Depends(AuthenticationService.get_current_user)
):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_district_service(db)
    else:
        return current_user


@router.get("/department", response_model=DepartmentListResponse)
async def get_advertisement_department(db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_department_service(db)
    else:
        return current_user
    
@router.get("/utility", response_model=UtilityListResponse)
async def get_advertisement_utility(db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_utility_service(db)
    else:
        return current_user




@router.get("/", response_model=AdPageResponse)
async def get_advertisements(filters: AdPageFilterSchema = Depends(), pagination: int = 0, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_filtered_advertisements_service(filters, db, pagination)
    else:
        return current_user


@router.post("/", response_model=AdPageResponse)
async def create_adpage(adpage: AdPageRequest, db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdvertisementService.create_adpage_service(adpage,db,user_id=current_user.userid)
    else:
        return current_user


@router.put("/{adpage_id}", response_model=AdPageResponse)
async def update_adpage(adpage_id: int, adpage: AdPageRequest, db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
       return AdvertisementService.update_adpage_service(adpage_id, adpage,db,user_id=current_user.userid) 
    else:
        return current_user    

@router.delete("/{adpage_id}", response_model=AdPageResponse)
async def delete_adpage(adpage_id: int, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        if current_user.role == True or current_user.userid == AdPageCRUD.get_userid_by_ad(db, adpage_id):
            return AdvertisementService.delete_adpage_service(adpage_id, db)
    else:
        return current_user    
    

@router.get("/{adpage_id}", response_model=AdPageResponse)
async def get_advertisement(adpage_id: int, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdvertisementService.get_ad_details_service(adpage_id, db)
    else:
        return current_user
    






    


    

    

    


