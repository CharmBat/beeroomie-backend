from typing import List
from schemas.Advertisement import AdvertisementFrontEnd, AdvertisementResponse





def create_response_multiple_ads( user_message: str, error_status: int, system_message: str,advertisement_list: List[AdvertisementFrontEnd] = None):
    return AdvertisementResponse(
        advertisement_list=advertisement_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

def create_response_single_ad( user_message: str, error_status: int, system_message: str,advertisement: AdvertisementFrontEnd = None):
    return AdvertisementResponse(
        advertisement=advertisement,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )