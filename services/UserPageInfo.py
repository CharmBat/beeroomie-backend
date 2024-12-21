from crud.UserPageInfo import UserPageInfoCRUD
from schemas.UserPageInfo import UserPageInfoSchema, UserPageInfoResponseSchema, UserPageInfoResponse
from fastapi import status
from utils.UserPageInfo import user_page_info_response


from crud.UserPageInfo import UserPageInfoCRUD
from schemas.UserPageInfo import UserPageInfoResponseSchema
from fastapi import status
from utils.UserPageInfo import user_page_info_response

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
    def create_user_page_info_service(user_page_info: UserPageInfoSchema, db):
        try:
            # Doğrulama
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
            # Doğrulama
            validated_user_info = UserPageInfoSchema.model_validate(user_page_info)
            updated_user_info = UserPageInfoCRUD.update(db, userid, validated_user_info)
            if not updated_user_info:
                return user_page_info_response(
                    user_message="UserPageInfo not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                    user_info_list=None,
                )
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

    @staticmethod
    def delete_user_page_info_service(userid: int, db):
        try:
            deleted_user_info = UserPageInfoCRUD.delete(db, userid)
            if not deleted_user_info:
                return user_page_info_response(
                    user_message="UserPageInfo not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No record found with the given ID",
                )
            return user_page_info_response(
                user_message=f"UserPageInfo for user {userid} deleted successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK",
            )
        except Exception as e:
            return user_page_info_response(
                user_message="Failed to delete UserPageInfo",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
            )
