from unittest.mock import patch, MagicMock
from services.Advertisement import AdvertisementService
from schemas.Advertisement import AdPageResponse, AdPageRequest, AdPageResponseSchema, AdPageFilterSchema, AdListingResponseSchema

class TestAdvertisementService:
    @patch('crud.Advertisement.AdPageCRUD.create')
    def test_create_adpage_service_success(self, mock_create_ad):
        mock_create_ad.return_value = MagicMock(adpageid=1)
        db = MagicMock()

        adpage_request = AdPageRequest(
            adpageid=0,
            title="Test Ad",
            price=1000,
            adtype=True,
            m2=120,
            n_floor=10,
            floornumber=2,
            pet=True,
            smoking=False,
            furnished=True,
            description="Test description",
            address="Test address",
            gender_choices=1,
            ad_date="2024-12-29",
            userid_fk=1,
            neighborhoodid_fk=1,
            n_roomid_fk=1,
            photos=[],
            utilites=[]
        )

        response = AdvertisementService.create_adpage_service(adpage_request, db, user_id=1)

        assert response.user_message == "Advertisement 1 created successfully"
        assert response.error_status == 201
    


    @patch('crud.Advertisement.AdPageCRUD.create')
    def test_create_adpage_service_failure(self, mock_create_ad):
        mock_create_ad.side_effect = Exception("Database error")

        db = MagicMock()

        adpage_request = AdPageRequest(
            adpageid=0,
            title="Test Ad",
            price=1000,
            adtype=True,
            m2=120,
            n_floor=10,
            floornumber=2,
            pet=True,
            smoking=False,
            furnished=True,
            description="Test description",
            address="Test address",
            gender_choices=1,
            ad_date="2024-12-29",
            userid_fk=1,
            neighborhoodid_fk=1,
            n_roomid_fk=1,
            photos=[],
            utilites=[]
        )

        response = AdvertisementService.create_adpage_service(adpage_request, db, user_id=1)

        assert response.user_message == "Failed to create Advertisement"
        assert response.error_status == 500
        assert "Database error" in response.system_message



    @patch('crud.Advertisement.AdPageCRUD.create')
    def test_create_adpage_service_database_error(self, mock_create_ad):
        mock_create_ad.side_effect = Exception("Database error")

        db = MagicMock()
        adpage_request = MagicMock(spec=AdPageRequest, photos=["photo1.jpg"], utilites=[1, 2])

        response = AdvertisementService.create_adpage_service(adpage_request, db, user_id=1)

        assert "Failed to create Advertisement" in response.user_message

    @patch('crud.Advertisement.AdPageCRUD.get_ad_by_id')
    def test_get_ad_details_service_success(self, mock_get_ad_by_id):
        mock_get_ad_by_id.return_value = MagicMock(
            adpageid=1,
            title="Test Ad",
            price=1000,
            adtype=True,
            m2=120,
            n_floor=10,
            floornumber=2,
            pet=True,
            smoking=False,
            furnished=True,
            description="Test Description",
            address="Test Address",
            gender_choices=1,
            ad_date="2024-12-29",
            neighborhood="Test Neighborhood",
            district="Test District",
            n_room="3+1",
            user_full_name="Test User",
            photos=["photo1.jpg", "photo2.jpg"],
            utilities=["Utility1", "Utility2"]
        )

        db = MagicMock()

        response = AdvertisementService.get_ad_details_service(1, db)

        assert response.user_message == "Advertisement fetched successfully"
        assert response.error_status == 200

        assert response.advertisement_list[0].adpageid == 1
        assert response.advertisement_list[0].title == "Test Ad"
        assert response.advertisement_list[0].neighborhood == "Test Neighborhood"
        assert response.advertisement_list[0].photos == ["photo1.jpg", "photo2.jpg"]

    @patch('crud.Advertisement.AdPageCRUD.get_ad_by_id')
    def test_get_ad_details_service_not_found(self, mock_get_ad_by_id):
        mock_get_ad_by_id.return_value = None
        db = MagicMock()
        response = AdvertisementService.get_ad_details_service(1, db)
        assert "Advertisement not found" in response.user_message


    @patch('crud.Advertisement.AdPageCRUD.get_filtered_ads')
    def test_get_filtered_advertisements_service_success(self, mock_get_filtered_ads):
        mock_get_filtered_ads.return_value = (
            [
                AdListingResponseSchema(
                    adpageid=1,
                    title="Test Ad",
                    price=1000,
                    adtype=True,
                    pet=True,
                    smoking=False,
                    address="Test Address",
                    full_name="John Doe",
                    photos=["photo1.jpg", "photo2.jpg"]
                ),
                AdListingResponseSchema(
                    adpageid=2,
                    title="Another Test Ad",
                    price=2000,
                    adtype=False,
                    pet=False,
                    smoking=True,
                    address="Another Address",
                    full_name="Jane Doe",
                    photos=["photo3.jpg"]
                )
            ],
            2  
        )

        db = MagicMock()
        filters = MagicMock(spec=AdPageFilterSchema)

        response = AdvertisementService.get_filtered_advertisements_service(filters, db, pagination=0)

        assert isinstance(response, AdPageResponse)
        assert response.user_message == "Advertisements fetched successfully."
        assert response.error_status == 200
        assert response.system_message == "Page 1, showing 2 of 2 advertisements."
        
        assert len(response.advertisement_list) == 2
        assert response.advertisement_list[0].adpageid == 1
        assert response.advertisement_list[0].title == "Test Ad"
        assert response.advertisement_list[1].adpageid == 2
        assert response.advertisement_list[1].title == "Another Test Ad"

        mock_get_filtered_ads.assert_called_once_with(db, filters.dict(exclude_unset=True), limit=10, offset=0)

    @patch('crud.Advertisement.AdPageCRUD.get_filtered_ads')
    def test_get_filtered_advertisements_service_failure(self, mock_get_filtered_ads):
        mock_get_filtered_ads.side_effect = Exception("Database error")

        db = MagicMock()
        filters = MagicMock(spec=AdPageFilterSchema)

        response = AdvertisementService.get_filtered_advertisements_service(filters, db, pagination=0)

        assert "Failed to retrieve advertisements." in response.user_message
