from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.Advertisement import AdvertisementResponse
from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageResponseSchema
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

@router.post("/", response_model=AdPageResponse)
def create_adpage(adpage: AdPageSchema, db: Session = Depends(get_db)):
    try:
        advertisement = AdPageCRUD.create(db, adpage)
        return AdPageResponse(
            advertisement_list=[advertisement],
            user_message=f"Advertisement {advertisement.adpageid} created successfully",
            error_status=0,
            system_message="OK"
        )
    except Exception as e:
        return AdPageResponse(
            advertisement_list=None,
            user_message="Failed to create Advertisement",
            error_status=500,
            system_message=str(e)
        )

@router.put("/{adpage_id}", response_model=AdPageResponse)
def update_adpage(adpage_id: int, adpage: AdPageSchema, db: Session = Depends(get_db)):
    try:
        db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
        if not db_adpage:
            return AdPageResponse(
                advertisement_list=None,
                user_message="Advertisement not found",
                error_status=404,
                system_message="No record found with the given ID"
            )

        updated_adpage = AdPageCRUD.update(db, adpage_id, adpage)
        return AdPageResponse(
            advertisement_list=[updated_adpage],
            user_message="Advertisement updated successfully",
            error_status=0,
            system_message="OK"
        )
    except Exception as e:
        return AdPageResponse(
            advertisement_list=None,
            user_message="Failed to update Advertisement",
            error_status=500,
            system_message=str(e)
        )
    
@router.delete("/{adpage_id}")
def delete_adpage(adpage_id: int, db: Session = Depends(get_db)):
    try:
   
        result = AdPageCRUD.delete(db, adpage_id)
        
        if not result:  
            return AdPageResponse(
                advertisement_list=None,
                user_message="Advertisement not found",
                error_status=404,
                system_message="No record found with the given ID"
            )
        
        return AdPageResponse(
            advertisement_list=None,
            user_message="Advertisement deleted successfully",
            error_status=0,
            system_message="OK"
        )
    except Exception as e:
        return AdPageResponse(
            advertisement_list=None,
            user_message="Failed to delete Advertisement",
            error_status=500,
            system_message=str(e)
        )


@router.get("/{adpage_id}", response_model=AdPageResponse)
def read_adpage(adpage_id: int, db: Session = Depends(get_db)):
    try:
        # İlanı getir
        db_adpage = AdPageCRUD.get_by_id(db, adpage_id)

        if not db_adpage:  
            return AdPageResponse(
                advertisement_list=None,
                user_message="Advertisement not found",
                error_status=404,
                system_message="No record found with the given ID"
            )

        response_data = AdPageResponseSchema.from_orm(db_adpage)

        return AdPageResponse(
            advertisement_list=[response_data],
            user_message="Advertisement fetched successfully",
            error_status=0,
            system_message="OK"
        )
    except Exception as e:
        return AdPageResponse(
            advertisement_list=None,
            user_message="Failed to fetch Advertisement",
            error_status=500,
            system_message=str(e)
        )
