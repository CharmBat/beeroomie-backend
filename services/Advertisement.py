from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageRequest, AdPageResponseSchema,AdPageFilterSchema, UtilityListResponse, UtilityResponseSchema, DepartmentListResponse, DepartmentResponseSchema
from schemas.Advertisement import DistrictListResponse, DistrictResponseSchema, NeighborhoodListResponse, NeighborhoodResponseSchema, NumberOfRoomListResponse, NumberOfRoomResponseSchema
from crud.Advertisement import AdDepartmentCRUD, AdPageCRUD,PhotosCRUD, AdUtilitiesCRUD, AdDistrictCRUD, AdNeighborhoodCRUD, AdNumberOfRoomCRUD
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
                    user_message="İlan bulunamadı",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                )

            # İlanın sahibi olan kullanıcıyı kontrol et
            if db_adpage.userid_fk != userid:
                return create_response_only_message(
                    user_message="Bu ilanı güncelleme yetkiniz yok",
                    error_status=status.HTTP_403_FORBIDDEN,
                    system_message="User is not the owner of the advertisement",
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
            utilities = AdUtilitiesCRUD.get_all_utilities(db)

            if not utilities:
                return UtilityListResponse(
                    user_message="No utilities found.",
                    system_message="No utilities available in the database.",
                    utilities=[]
                )
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





    @staticmethod
    def get_department_service(db) -> DepartmentListResponse:
        try:
            departments = AdDepartmentCRUD.get_all_departments(db)

            if not departments:
                return DepartmentListResponse(
                    user_message="No departments found.",
                    system_message="No departments available in the database.",
                    departments=[]
                )

            department_list = [
                DepartmentResponseSchema(
                    departmentid=department.departmentid,
                    department_name=department.department_name
                )
                for department in departments
            ]

            return DepartmentListResponse(
                user_message="Departments fetched successfully.",
                system_message="OK",
                departments=department_list
            )
        except Exception as e:
            return DepartmentListResponse(
                user_message="Failed to fetch departments.",
                system_message=str(e),
                departments=[]
            )
        
    
    @staticmethod
    def get_district_service(db) -> DistrictListResponse:
        try:
            districts = AdDistrictCRUD.get_all_districts(db)

            if not districts:
                return DistrictListResponse(
                    user_message="No districts found.",
                    system_message="No districts available in the database.",
                    districts=[]
                )

            district_list = [
                DistrictResponseSchema(
                    districtid=district.districtid,
                    district_name=district.district_name
                )
                for district in districts
            ]

            return DistrictListResponse(
                user_message="Districts fetched successfully.",
                system_message="OK",
                districts=district_list
            )
        except Exception as e:
            return DistrictListResponse(
                user_message="Failed to fetch districts.",
                system_message=str(e),
                districts=[]
            )
        


    @staticmethod
    def get_neighborhoods_by_district_service(db, district_id: int) -> NeighborhoodListResponse:
        try:
            neighborhoods = AdNeighborhoodCRUD.get_neighborhoods_by_district(db, district_id)

            if not neighborhoods:
                return NeighborhoodListResponse(
                    user_message=f"No neighborhoods found for district_id {district_id}.",
                    system_message="No neighborhoods available for the given district.",
                    neighborhoods=[]
                )

            neighborhood_list = [
                NeighborhoodResponseSchema(
                    neighborhoodid=neighborhood.neighborhoodid,
                    neighborhood_name=neighborhood.neighborhood_name
                )
                for neighborhood in neighborhoods
            ]

            return NeighborhoodListResponse(
                user_message="Neighborhoods fetched successfully.",
                system_message="OK",
                neighborhoods=neighborhood_list
            )
        except Exception as e:
            return NeighborhoodListResponse(
                user_message="Failed to fetch neighborhoods.",
                system_message=str(e),
                neighborhoods=[]
            )
        

    @staticmethod
    def get_all_rooms_service(db) -> NumberOfRoomListResponse:
        try:
            rooms = AdNumberOfRoomCRUD.get_all_rooms(db)

            if not rooms:
                return NumberOfRoomListResponse(
                    user_message="No rooms found.",
                    system_message="No rooms available in the database.",
                    rooms=[]
                )

            room_list = [
                NumberOfRoomResponseSchema(
                    n_roomid=room.n_roomid,
                    n_room=room.n_room
                )
                for room in rooms
            ]

            return NumberOfRoomListResponse(
                user_message="Rooms fetched successfully.",
                system_message="OK",
                rooms=room_list
            )
        except Exception as e:
            return NumberOfRoomListResponse(
                user_message="Failed to fetch rooms.",
                system_message=str(e),
                rooms=[]
            )

