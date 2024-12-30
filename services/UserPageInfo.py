from crud.UserPageInfo import UserPageInfoCRUD
from schemas.UserPageInfo import UserPageInfoSchema
from fastapi import status
from utils.UserPageInfo import user_page_info_response
from services.PhotoHandle import PhotoHandleService
from crud.Authentication import AuthCRUD
from utils.Authentication import create_response_user_me
from schemas.Authentication import UserMe
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
            validated_user_info = UserPageInfoSchema.model_validate(user_page_info)
            validated_user_info.userid_fk = user_id
            
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
            # Önce kullanıcı bilgilerini al
            user_info = UserPageInfoCRUD.get_by_userid(db, userid)
            if not user_info:
                return user_page_info_response(
                    user_message="User not found.",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="User not found."
                )

            # Profil fotoğrafı varsa sil
            if user_info.ppurl:
                PhotoHandleService.photo_delete_service(user_info.ppurl)

            # Kullanıcıyı sil
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
                    system_message="No record found with the given ID"
                )
            user=UserMe(userid=userid,role=role,full_name=user_info.full_name,rh=user_info.rh,ppurl=user_info.ppurl)#is confirmed not authenticaed is_profile_complete not found
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
