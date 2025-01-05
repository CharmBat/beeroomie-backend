from crud.UserPageInfo import UserPageInfoCRUD
from schemas.UserPageInfo import UserPageInfoSchema
from fastapi import status
from utils.UserPageInfo import user_page_info_response
from services.PhotoHandle import PhotoHandleService
from crud.Authentication import AuthCRUD
from utils.Authentication import create_response_user_me
from schemas.Authentication import UserMe
from models.Advertisement import AdPage, Photos
from crud.Advertisement import AdPageCRUD

class UserPageInfoService:
    @staticmethod
    def get_user_page_info_service(userid: int, db):
        """
        Fetches UserPageInfo by user ID.
        """
        try:
            user_info = UserPageInfoCRUD.get_user_info_by_id(db, userid)
            if not user_info:
                return user_page_info_response(
                    user_message="UserPageInfo not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                    user_info_list=None,
                )
            return user_page_info_response(
                user_message="UserPageInfo retrieved successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
                user_info_list=[user_info],  # ResponseSchema already matches the expected format
            )
        except Exception as e:
            return user_page_info_response(
                user_message="Failed to retrieve UserPageInfo",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                user_info_list=None,
            )

    @staticmethod
    def create_user_page_info_service(user_page_info: UserPageInfoSchema, db, user_id):
        try:
            user_page_info.userid_fk = user_id
            validated_user_info = UserPageInfoSchema.model_validate(user_page_info)
            created_user_info = UserPageInfoCRUD.create(db, validated_user_info)
            return user_page_info_response(
                user_message=f"UserPageInfo created successfully for user {created_user_info.userid_fk}",
                error_status=status.HTTP_201_CREATED,
                system_message="OK",
                # user_info_list=[UserPageInfoResponseSchema.from_orm(created_user_info)],
            )
        except Exception as e:
            return user_page_info_response(
                user_message="Failed to create UserPageInfo",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                user_info_list=None,
            )

    @staticmethod
    def update_user_page_info_service(userid: int, user_page_info: UserPageInfoSchema, db):
        try:
            # Mevcut kullanıcı bilgilerini al
            existing_user_info = UserPageInfoCRUD.get_by_userid(db, userid)
            if not existing_user_info:
                return user_page_info_response(
                    user_message="UserPageInfo not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                    user_info_list=None,
                )

            user_page_info.userid_fk = userid
            validated_user_info = UserPageInfoSchema.model_validate(user_page_info)
            
            # Sadece eski fotoğraf varsa ve yeni fotoğraf farklıysa sil
            if existing_user_info.ppurl and validated_user_info.ppurl != existing_user_info.ppurl:
                PhotoHandleService.photo_delete_service(existing_user_info.ppurl)

            updated_user_info = UserPageInfoCRUD.update(db, userid, validated_user_info)
                
            return user_page_info_response(
                user_message="UserPageInfo updated successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
                # user_info_list=[UserPageInfoResponseSchema.from_orm(updated_user_info)],
            )
        except Exception as e:
            return user_page_info_response(
                user_message="Failed to update UserPageInfo",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                user_info_list=None,
            )

    # @staticmethod
    # def delete_user_page_info_service(userid: int, db):
    #     try:
    #         deleted_user_info = UserPageInfoCRUD.delete(db, userid)
    #         if not deleted_user_info:
    #             return user_page_info_response(
    #                 user_message="UserPageInfo not found",
    #                 error_status=status.HTTP_404_NOT_FOUND,
    #                 system_message="No record found with the given ID",
    #             )
    #         if deleted_user_info.ppurl:
    #             PhotoHandleService.photo_delete_service(deleted_user_info.ppurl)

    #         return user_page_info_response(
    #             user_message=f"UserPageInfo for user {userid} deleted successfully",
    #             error_status=status.HTTP_200_OK,
    #             system_message="OK",
    #         )
    #     except Exception as e:
    #         return user_page_info_response(
    #             user_message="Failed to delete UserPageInfo",
    #             error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             system_message=str(e),
    #         )
    @staticmethod
    def delete_user_service(userid, db):
        try:
            # Get user info
            user_info = UserPageInfoCRUD.get_by_userid(db, userid)
            if not user_info:
                return user_page_info_response(
                    user_message="Kullanıcı bulunamadı",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="User not found."
                )

            # If user is a housie (rh=True), delete their advertisement photos
            if user_info.rh:
                # Get user's advertisement
                advertisement = db.query(AdPage).filter(AdPage.userid_fk == userid).first()
                if advertisement:
                    # Get all photos for this advertisement
                    photos = db.query(Photos).filter(Photos.adpageid_fk == advertisement.adpageid).all()
                    # Delete each photo from Cloudinary
                    for photo in photos:
                        if photo.photourl:
                            PhotoHandleService.photo_delete_service(photo.photourl)

            # Delete profile picture if exists
            if user_info.ppurl:
                PhotoHandleService.photo_delete_service(user_info.ppurl)

            # Delete user
            AuthCRUD.delete_user(userid, db)
            
            return user_page_info_response(
                user_message="User deleted successfully.",
                error_status=status.HTTP_201_CREATED,
                system_message="User deleted successfully."
            ) 
        
        except Exception as e:
            print(f"Invalid userid or deletion failed: {e}")
            return user_page_info_response(
                user_message="Invalid userid or deletion failed.",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message=str(e)
            )

    @staticmethod
    def current_user_service(userid,role,db):
        try:
            user_info = UserPageInfoCRUD.get_user_info_by_id(db, userid)
            
            if not user_info:
                return create_response_user_me(
                    user_message="UserPageInfo not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                    user = UserMe(userid=userid,role=None,full_name=None,rh=None,ppurl=None,adv_id=None)
                )
            
            rh=user_info.rh            
            adv_id=None

            if rh==True:
                adv_id=AdPageCRUD.get_ad_id_by_user_id(db,userid)
            user=UserMe(userid=userid,role=role,full_name=user_info.full_name,rh=rh,ppurl=user_info.ppurl,adv_id=adv_id)#is confirmed not authenticaed is_profile_complete not found
            
            return create_response_user_me(
                user_message="UserPageInfo retrieved successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
                user=user,
            )
        except Exception as e:
            return create_response_user_me(
                user_message="Failed to retrieve UserPageInfo",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e)
            )
