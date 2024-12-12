from schemas.Advertisement import AdPageSchema, AdPageResponse
from crud.Advertisement import AdPageCRUD
from fastapi import status
from utils.Advertisement import create_response_ads

class AdvertisementService:

    @staticmethod
    def create_adpage_service(adpage: AdPageSchema, db):
        try:
            advertisement = AdPageCRUD.create(db, adpage)
            return create_response_ads(
                user_message=f"Advertisement {advertisement.adpageid} created successfully",
                error_status=status.HTTP_201_CREATED, 
                system_message="OK",
                advertisement_list=[advertisement]
            )
        except Exception as e:
            return create_response_ads(
                user_message="Failed to create Advertisement",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,  
                system_message=str(e),
                advertisement_list=None
            )

    @staticmethod
    def update_adpage_service(adpage_id: int, adpage: AdPageSchema, db):
        try:
            db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
            if not db_adpage:
                return create_response_ads(
                    user_message="Advertisement not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                    advertisement_list=None
                )

            updated_adpage = AdPageCRUD.update(db, adpage_id, adpage)
            return create_response_ads(
                user_message="Advertisement updated successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
                advertisement_list=[updated_adpage]
            )
        except Exception as e:
            return create_response_ads(
                user_message="Failed to update Advertisement",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                system_message=str(e),
                advertisement_list=None
            )

