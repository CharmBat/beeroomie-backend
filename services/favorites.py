from crud.favorites import favoritesCRUD
from utils.Advertisement import create_response_ads_listing
from fastapi import status

class favoritesService:
    @staticmethod
    def get_user_favorites(user_id: int, db, pagination: int):
        try:
            limit = 10
            offset = pagination * limit

            favoriteAds, total_count = favoritesCRUD.get_user_favorites(db, user_id, limit=limit, offset=offset)

            return create_response_ads_listing(
                user_message="Advertisements fetched successfully.",
                error_status=status.HTTP_200_OK,
                system_message=f"Page {pagination + 1}, showing {len(favoriteAds)} of {total_count} advertisements.",
                advertisement_list=favoriteAds
            )
        except Exception as e:
            return create_response_ads_listing(
                user_message="Failed to retrieve advertisements.",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                advertisement_list=None
            )

    @staticmethod
    def add_to_favorites(user_id: int, adpage_id: int, db):
        try:
            favoritesCRUD.add_to_favorites(db, user_id, adpage_id)

            return create_response_ads_listing(
                user_message="Advertisement added to favorites successfully.",
                error_status=status.HTTP_200_OK,
                system_message="Advertisement added to favorites successfully.",
                advertisement_list=None
            )
        except Exception as e:
            return create_response_ads_listing(
                user_message="An unexpected error occurred.",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                advertisement_list=None
            )

    @staticmethod
    def remove_from_favorites(user_id: int, adpage_id: int, db):
        try:
            favoritesCRUD.remove_from_favorites(db, user_id, adpage_id)

            return create_response_ads_listing(
                user_message="Advertisement removed from favorites successfully.",
                error_status=status.HTTP_200_OK,
                system_message="Advertisement removed from favorites successfully.",
                advertisement_list=None
            )
        except Exception as e:
            return create_response_ads_listing(
                user_message="An unexpected error occurred.",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                advertisement_list=None
            )




