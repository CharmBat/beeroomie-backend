from typing import List
from schemas.Advertisement import AdPageResponseSchema, AdPageResponse, AdListingResponseSchema

# def create_response_ads(user_message: str, error_status: int, system_message: str, advertisement_list: List[AdPageResponseSchema] = None):
#     return AdPageResponse(
#         advertisement_list=advertisement_list,
#         user_message=user_message,
#         error_status=error_status,
#         system_message=system_message
#     )

def create_response_only_message(user_message: str, error_status: int, system_message: str):
    return AdPageResponse(
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

def create_response_ads_listing(user_message: str, error_status: int, system_message: str, advertisement_list: List[AdListingResponseSchema] = None):
    return AdPageResponse(
        advertisement_list=advertisement_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
   )