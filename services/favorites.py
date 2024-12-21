from crud.favorites import favoritesCRUD
from utils.Advertisement import create_response_ads_listing


class favoritesService:
    @staticmethod
    def get_user_favorites(user_id: int, db, pagination: int):
        try:
            limit = 10 
            offset = pagination * limit

            favoriteAds, total_count = favoritesCRUD.get_user_favorites(db, user_id, limit=limit, offset=offset)

            return create_response_ads_listing(
                user_message="Advertisements fetched successfully.",
                error_status=200,
                system_message=f"Page {pagination + 1}, showing {len(favoriteAds)} of {total_count} advertisements.",
                advertisement_list=favoriteAds
            )
        except Exception as e:
            return create_response_ads_listing(
                user_message="Failed to retrieve advertisements.",
                error_status=500,
                system_message=str(e),
                advertisement_list=None
            )
        

    @staticmethod
    def add_to_favorites(user_id: int, adpage_id: int, db):
        try:
            response = favoritesCRUD.add_to_favorites(db, user_id, adpage_id)
            
            if response["status"] == 200:
                return {
                    "user_message": "Advertisement added to favorites successfully.",
                    "error_status": 200,
                    "system_message": "OK"
                }
            else:
                return {
                    "user_message": "Failed to add advertisement to favorites.",
                    "error_status": response["status"],
                    "system_message": response["message"]
                }
        except Exception as e:
            return {
                "user_message": "An unexpected error occurred.",
                "error_status": 500,
                "system_message": str(e)
            }



