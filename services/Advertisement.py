from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageRequest, AdPageResponseSchema,AdPageFilterSchema
from crud.Advertisement import AdPageCRUD,PhotosCRUD,AdUtilitiesCRUD
from fastapi import status
from utils.Advertisement import create_response_ads_listing,create_response_only_message
from services.PhotoHandle import PhotoHandleService

class AdvertisementService:

 from crud.Advertisement import PhotosCRUD, AdUtilitiesCRUD

class AdvertisementService:
    @staticmethod
    def create_adpage_service(adpage: AdPageRequest, db, user_id: int):
        try:
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
            # Photos ekle
            if adpage.photos:
                photo_urls = []
                for photo in adpage.photos:
                    photo_url = PhotoHandleService.photo_upload_service(photo)
                    if photo_url:
                        photo_urls.append(photo_url)
                PhotosCRUD.create_photos(db, advertisement.adpageid, photo_urls)
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

            # Sadece AdPageSchema ile ilgili alanları filtrele
            adpage_schema_data = adpage.model_dump(exclude={"photos", "utilites"})
            adpage_schema_data["userid"] = userid
            # AdPageSchema nesnesine dönüştür
            adpage_schema = AdPageSchema(**adpage_schema_data)

            # Advertisement'ı güncelle
            updated_adpage = AdPageCRUD.update(db, adpage_id, adpage_schema)

            # Eski fotoğrafları sil
            old_photos = PhotosCRUD.get_photos_by_adpage_id(db, adpage_id)
            for photo in old_photos:
                PhotoHandleService.photo_delete_service(photo.photourl)
            PhotosCRUD.delete_photos(db, adpage_id)

            # Yeni fotoğrafları yükle
            if adpage.photos:
                photo_urls = []
                for photo in adpage.photos:
                    photo_url = PhotoHandleService.photo_upload_service(photo)
                    if photo_url:
                        photo_urls.append(photo_url)
                PhotosCRUD.create_photos(db, adpage_id, photo_urls)

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

            # İlana ait fotoğrafları bul ve PhotoHandleService ile sil
            photos = PhotosCRUD.get_photos_by_adpage_id(db, adpage_id)
            for photo in photos:
                PhotoHandleService.photo_delete_service(photo.photourl)

            # İlanı sil (cascade ile diğer veriler otomatik silinecek)
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

