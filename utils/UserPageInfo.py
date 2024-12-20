from typing import List, Optional
from schemas.UserPageInfo import UserPageInfoResponseSchema, UserPageInfoResponse


def user_page_info_response(
    user_message: str,
    error_status: int,
    system_message: str,
    user_info_list: Optional[List[UserPageInfoResponseSchema]] = None
) -> UserPageInfoResponse:
    return UserPageInfoResponse(
        user_info_list=user_info_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )