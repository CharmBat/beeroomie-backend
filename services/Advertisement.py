from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageRequest, AdPageResponseSchema,AdPageFilterSchema
from crud.Advertisement import AdPageCRUD,PhotosCRUD,AdUtilitiesCRUD
from fastapi import status
from utils.Advertisement import create_response_ads_listing,create_response_only_message

class AdvertisementService:

 from crud.Advertisement import PhotosCRUD, AdUtilitiesCRUD

class AdvertisementService:
    @staticmethod
    def create_adpage_service(adpage: AdPageRequest, db, user_id: int):
        try:
            # Sadece AdPageSchema ile ilgili alanları filtrele
            adpage_schema_data = adpage.model_dump(exclude={"photos", "utilites"})
            adpage_schema_data["userid"] = user_id
            # AdPageSchema nesnesine dönüştür
            adpage_schema = AdPageSchema(**adpage_schema_data)

            # Advertisement oluştur
            advertisement = AdPageCRUD.create(db, adpage_schema)
            # Photos ekle
            if adpage.photos:
                PhotosCRUD.create_photos(db, advertisement.adpageid, adpage.photos)
            # Ad Utilities ekle
            if adpage.utilites:
                AdUtilitiesCRUD.create_ad_utilities(db, advertisement.adpageid, adpage.utilites)

            return create_response_only_message(
                user_message=f"Advertisement {advertisement.adpageid} created successfully",
                error_status=status.HTTP_201_CREATED,
                system_message="OK",
            )
        except Exception as e:
            return create_response_only_message(
                user_message="Failed to create Advertisement",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e)
            )


    @staticmethod
    def update_adpage_service(adpage_id: int, adpage: AdPageRequest, db, userid: int):
        try:
            # Advertisement'ı ID ile kontrol et
            db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
            if not db_adpage:
                return create_response_only_message(
                    user_message="Advertisement not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                )

            # Sadece AdPageSchema ile ilgili alanları filtrele
            adpage_schema_data = adpage.model_dump(exclude={"photos", "utilites"})
            adpage_schema_data["userid"] = userid
            # AdPageSchema nesnesine dönüştür
            adpage_schema = AdPageSchema(**adpage_schema_data)

            # Advertisement'ı güncelle
            updated_adpage = AdPageCRUD.update(db, adpage_id, adpage_schema)

            # Photos güncelle
            PhotosCRUD.delete_photos(db, adpage_id)  # Eski fotoğrafları sil
            if adpage.photos:
                PhotosCRUD.create_photos(db, adpage_id, adpage.photos)

            # Ad Utilities güncelle
            AdUtilitiesCRUD.delete_ad_utilities(db, adpage_id)  # Eski utilities'i sil
            if adpage.utilites:
                AdUtilitiesCRUD.create_ad_utilities(db, adpage_id, adpage.utilites)

            return create_response_only_message(
                user_message=f"Advertisement {adpage_id} updated successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
            )
        except Exception as e:
            return create_response_only_message(
                user_message="Failed to update Advertisement",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
            )

    # @staticmethod
    # def get_all_advertisements_service(pagination,db) -> AdPageResponse:
    #     try:

    #         advertisement_list = AdPageCRUD.get_all(pagination=pagination,db=db)
    #         return create_response_ads_listing(
    #             user_message=f"Advertisements fetched successfully. Page: {pagination}",
    #             error_status=status.HTTP_200_OK, 
    #             system_message="OK",
    #             advertisement_list=advertisement_list
    #         )
    #     except Exception as e:
    #         return create_response_ads_listing(
    #             user_message="Failed to retrieve advertisements",
    #             error_status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
    #             system_message=str(e),
    #             advertisement_list=None
    #         )
     

    @staticmethod
    def delete_adpage_service(adpage_id: int, db) -> AdPageResponse:
        try:
            db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
            if not db_adpage:
                return create_response_only_message(
                    user_message="Advertisement not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                )

            AdPageCRUD.delete(db, adpage_id)
            return create_response_only_message(
                user_message=f"Advertisement {adpage_id} deleted successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
            )
        except Exception as e:
            return create_response_only_message(
                user_message="Failed to delete Advertisement",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
            )

    @staticmethod
    def get_ad_details_service(adpage_id: int, db) -> AdPageResponseSchema:
        try:
            ad = AdPageCRUD.get_ad_by_id(db, adpage_id)
    
            if not ad:
                return create_response_only_message(
                    user_message="Advertisement not found",
                    error_status=404,
                    system_message="No advertisement found with the given ID",
                )
    
            return create_response_only_message(
                user_message="Advertisement fetched successfully",
                error_status=200,
                system_message="OK",
                advertisement_list=[ad],  
            )
        except Exception as e:
            return create_response_only_message(
                user_message="Failed to fetch advertisement",
                error_status=500,
                system_message=str(e),
            )


    @staticmethod
    def get_filtered_advertisements_service(filters: AdPageFilterSchema, db, pagination: int):
        try:
            filters_dict = filters.dict(exclude_unset=True)

            limit = 10  
            offset = pagination * limit

            advertisements, total_count = AdPageCRUD.get_filtered_ads(db, filters_dict, limit=limit, offset=offset)

        
            return create_response_ads_listing(
                user_message="Advertisements fetched successfully.",
                error_status=200,
                system_message=f"Page {pagination + 1}, showing {len(advertisements)} of {total_count} advertisements.",
                advertisement_list=advertisements
            )
        except Exception as e:
            return create_response_ads_listing(
                user_message="Failed to retrieve advertisements.",
                error_status=500,
                system_message=str(e),
                advertisement_list=None
            )

