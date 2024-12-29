from unittest.mock import patch, MagicMock
from services.favorites import favoritesService
from schemas.Advertisement import AdPageResponse, AdListingResponseSchema

class TestFavoritesService:
    # get_user_favorites 

    @patch('services.favorites.favoritesCRUD.get_user_favorites')
    def test_get_user_favorites_success(self, mock_get_favorites):
        mock_get_favorites.return_value = (
            [
                {
                    "adpageid": 1,
                    "title": "Test Ad",
                    "address": "Test Address",
                    "pet": True,
                    "smoking": False,
                    "price": 1000,
                    "adtype": True,
                    "full_name": "John Doe",
                    "photos": ["photo1.jpg", "photo2.jpg"]
                }
            ],
            1
        )

        db = MagicMock()
        response = favoritesService.get_user_favorites(user_id=1, db=db, pagination=0)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 200
        assert len(response.advertisement_list) == 1

        ad_response = response.advertisement_list[0]
        assert isinstance(ad_response, AdListingResponseSchema)
        assert ad_response.adpageid == 1
        assert ad_response.title == "Test Ad"

    @patch('services.favorites.favoritesCRUD.get_user_favorites')
    def test_get_user_favorites_no_results(self, mock_get_favorites):
        mock_get_favorites.return_value = ([], 0)

        db = MagicMock()
        response = favoritesService.get_user_favorites(user_id=1, db=db, pagination=0)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 200
        assert response.advertisement_list == []
        assert response.system_message == "Page 1, showing 0 of 0 advertisements."

    @patch('services.favorites.favoritesCRUD.get_user_favorites')
    def test_get_user_favorites_database_error(self, mock_get_favorites):
        mock_get_favorites.side_effect = Exception("Database error")

        db = MagicMock()
        response = favoritesService.get_user_favorites(user_id=1, db=db, pagination=0)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 500
        assert response.advertisement_list is None
        assert "Database error" in response.system_message



    # add_to_favorites 


    @patch('services.favorites.favoritesCRUD.add_to_favorites')
    def test_add_to_favorites_success(self, mock_add_favorite):
        mock_add_favorite.return_value = None

        db = MagicMock()
        response = favoritesService.add_to_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 200
        assert response.user_message == "Advertisement added to favorites successfully."
        assert response.advertisement_list is None

    @patch('services.favorites.favoritesCRUD.add_to_favorites')
    def test_add_to_favorites_duplicate(self, mock_add_favorite):
        mock_add_favorite.side_effect = Exception("Unique constraint violated")

        db = MagicMock()
        response = favoritesService.add_to_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 500
        assert "Unique constraint violated" in response.system_message
        assert response.advertisement_list is None

    @patch('services.favorites.favoritesCRUD.add_to_favorites')
    def test_add_to_favorites_database_error(self, mock_add_favorite):
        mock_add_favorite.side_effect = Exception("Database error")

        db = MagicMock()
        response = favoritesService.add_to_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 500
        assert "Database error" in response.system_message
        assert response.advertisement_list is None


    # remove_from_favorites 



    @patch('services.favorites.favoritesCRUD.remove_from_favorites')
    def test_remove_from_favorites_success(self, mock_remove_favorite):
        mock_remove_favorite.return_value = None

        db = MagicMock()
        response = favoritesService.remove_from_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 200
        assert response.user_message == "Advertisement removed from favorites successfully."
        assert response.advertisement_list is None

    @patch('services.favorites.favoritesCRUD.remove_from_favorites')
    def test_remove_from_favorites_not_found(self, mock_remove_favorite):
        mock_remove_favorite.side_effect = Exception("Favorite not found")

        db = MagicMock()
        response = favoritesService.remove_from_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 500
        assert "Favorite not found" in response.system_message
        assert response.advertisement_list is None

    @patch('services.favorites.favoritesCRUD.remove_from_favorites')
    def test_remove_from_favorites_database_error(self, mock_remove_favorite):
        mock_remove_favorite.side_effect = Exception("Database error")

        db = MagicMock()
        response = favoritesService.remove_from_favorites(user_id=1, adpage_id=101, db=db)

        assert isinstance(response, AdPageResponse)
        assert response.error_status == 500
        assert "Database error" in response.system_message
        assert response.advertisement_list is None
