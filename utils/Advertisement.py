from typing import List
from schemas.Advertisement import AdPageResponseSchema, AdPageResponse
def create_response_ads(user_message: str, error_status: int, system_message: str, advertisement_list: List[AdPageResponseSchema] = None):
    return AdPageResponse(
        advertisement_list=advertisement_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )
