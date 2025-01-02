from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageRequest, AdPageResponseSchema,AdPageFilterSchema, UtilityListResponse, UtilityResponseSchema
from crud.Advertisement import AdPageCRUD,PhotosCRUD,AdUtilitiesCRUD
from fastapi import status
from utils.Advertisement import create_response_ads_listing,create_response_only_message
from services.PhotoHandle import PhotoHandleService
from crud.UserPageInfo import UserPageInfoCRUD
from models.Advertisement import AdPage

class AdvertisementService:
    @staticmethod
    def create_adpage_service(adpage: AdPageRequest, db, user_id: int):
        try:
            # Check if user already has an advertisement
            existing_user_ad = db.query(AdPage).filter(AdPage.userid_fk == user_id).first()
            if existing_user_ad:
                return create_response_only_message(
                    user_message="You already have an active advertisement. Please delete your existing advertisement before creating a new one.",
                    error_status=status.HTTP_400_BAD_REQUEST,
                    system_message="User already has an advertisement",
                )

            # Aynı başlıkta ilan var mı kontrol et
            existing_ad = AdPageCRUD.get_by_title(db, adpage.title)
            if existing_ad:
                return create_response_only_message(
                    user_message="An advertisement with this title already exists",
                    error_status=status.HTTP_400_BAD_REQUEST,
                    system_message="Duplicate title",
                )

            # Sadece AdPageSchema ile ilgili alanları filtrele
            adpage_schema_data = adpage.model_dump(exclude={"photos", "utilites"})
            adpage_schema_data["userid"] = user_id
            # AdPageSchema nesnesine dönüştür
            adpage_schema = AdPageSchema(**adpage_schema_data)

            # Advertisement oluştur
            advertisement = AdPageCRUD.create(db, adpage_schema)

            #Set RH status
            UserPageInfoCRUD.set_rh_status(db,user_id,True)#1 means housie

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

            # Aynı başlıkta başka bir ilan var mı kontrol et
            existing_ad = AdPageCRUD.get_by_title(db, adpage.title)
            if existing_ad and existing_ad.adpageid != adpage_id:
                return create_response_only_message(
                    user_message="An advertisement with this title already exists",
                    error_status=status.HTTP_400_BAD_REQUEST,
                    system_message="Duplicate title",
                )

            # Advertisement'ı güncelle
            adpage_schema_data = adpage.model_dump(exclude={"photos", "utilites"})
            adpage_schema_data["userid"] = userid
            adpage_schema = AdPageSchema(**adpage_schema_data)
            updated_adpage = AdPageCRUD.update(db, adpage_id, adpage_schema)

            # Ad Utilities güncelle
            AdUtilitiesCRUD.delete_ad_utilities(db, adpage_id)
            if adpage.utilites:
                AdUtilitiesCRUD.create_ad_utilities(db, adpage_id, adpage.utilites)

            # Eski fotoğrafları sil
            old_photos = PhotosCRUD.get_photos_by_adpage_id(db, adpage_id)
            for photo in old_photos:
                PhotoHandleService.photo_delete_service(photo.photourl)
            PhotosCRUD.delete_photos(db, adpage_id)

            # Yeni fotoğraf URL'lerini kaydet
            if adpage.photos:
                PhotosCRUD.create_photos(db, adpage_id, adpage.photos)

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
            # İlanı kontrol et
            db_adpage = AdPageCRUD.get_by_id(db, adpage_id)
            if not db_adpage:
                return create_response_only_message(
                    user_message="Advertisement not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                )

            # İlana ait fotoğrafları bul ve sil
            photos = PhotosCRUD.get_photos_by_adpage_id(db, adpage_id)
            for photo in photos:
                PhotoHandleService.photo_delete_service(photo.photourl)

            # İlanı sil (cascade ile diğer veriler otomatik silinecek)
            adv_owner= AdPageCRUD.get_userid_by_ad(db,adpage_id)
            UserPageInfoCRUD.set_rh_status(db,adv_owner,False)#0 means roomie

            AdPageCRUD.delete(db, adpage_id)

            return create_response_only_message(
                user_message=f"Advertisement {adpage_id} and all related data deleted successfully",
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




    @staticmethod
    def get_utility_service(db) -> UtilityListResponse:
        try:
            # Tüm utilities verilerini çek
            utilities = AdUtilitiesCRUD.get_all_utilities(db)

            if not utilities:
                return UtilityListResponse(
                    user_message="No utilities found.",
                    system_message="No utilities available in the database.",
                    utilities=[]
                )

            # Verileri listeye dönüştür
            utilities_list = [
                UtilityResponseSchema(
                    utilityid=utility.utilityid,
                    utility_name=utility.utility_name
                )
                for utility in utilities
            ]

            return UtilityListResponse(
                user_message="Utilities fetched successfully.",
                system_message="OK",
                utilities=utilities_list
            )
        except Exception as e:
            return UtilityListResponse(
                user_message="Failed to fetch utilities.",
                system_message=str(e),
                utilities=[]
            )
