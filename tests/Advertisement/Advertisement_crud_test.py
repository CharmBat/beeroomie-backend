from unittest.mock import MagicMock
from datetime import datetime
from models.Advertisement import AdPage
from schemas.Advertisement import AdPageSchema
from crud.Advertisement import AdPageCRUD, PhotosCRUD, AdUtilitiesCRUD
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
import pytest


class TestAdPageCRUD:
    def test_get_ad_by_id_success(self):
        # Setup mock DB and return values
        db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_query.first.return_value = MagicMock(
            adpageid=1,
            title="Test Ad",
            price=1000,
            adtype=True,
            m2=100,
            n_floor=5,
            floornumber=3,
            pet=True,
            smoking=False,
            furnished=True,
            description="Test description",
            address="Test address",
            gender_choices=1,
            ad_date=datetime.now().date(),
            neighborhood="Test neighborhood",
            district="Test district",
            n_room="2+1",
            user_full_name="Test User"
        )
        db.query.return_value.join.return_value.join.return_value.join.return_value.join.return_value.filter.return_value = mock_query

        # Mock photos and utilities queries
        photo_query = MagicMock()
        photo_query.all.return_value = [MagicMock(photourl="test1.jpg"), MagicMock(photourl="test2.jpg")]
        db.query().filter.return_value = photo_query

        utility_query = MagicMock()
        utility_query.all.return_value = [MagicMock(utility_name="Internet"), MagicMock(utility_name="Water")]
        db.query().join().filter.return_value = utility_query

        result = AdPageCRUD.get_ad_by_id(db, 1)
        
        assert result is not None
        assert result.adpageid == 1
        assert result.title == "Test Ad"
        assert len(result.photos) == 2
        assert len(result.utilities) == 2

    def test_get_ad_by_id_failure(self):
        db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_query.first.return_value = None
        db.query.return_value.join.return_value.join.return_value.join.return_value.join.return_value.filter.return_value = mock_query

        result = AdPageCRUD.get_ad_by_id(db, 999)
        assert result is None

    def test_get_filtered_ads_success(self):
        db = MagicMock(spec=Session)

        # Mock ad query result
        ad_query_result = [
            MagicMock(
                adpageid=1,
                title="Test Ad",
                price=1000,
                adtype=True,
                address="Test Address",
                pet=True,
                smoking=False,
                full_name="Test User"
            )
        ]
        photo_query_result = [
            MagicMock(adpageid_fk=1, photourl="test.jpg")
        ]
        query_mock = db.query.return_value
        query_mock.join.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value.limit.return_value.all.return_value = ad_query_result

        photo_mock = db.query.return_value
        photo_mock.filter.return_value.all.return_value = photo_query_result

        filters = {"min_price": 500, "max_price": 1500}
        results, count = AdPageCRUD.get_filtered_ads(db, filters)

        assert len(results) == 1
        assert results[0].adpageid == 1
        assert results[0].title == "Test Ad"
        assert results[0].photos == ["test.jpg"]
        assert count == 1

    def test_get_by_id_success(self):
            db = MagicMock(spec=Session)
            mock_ad = AdPage(
                adpageid=1,
                title="Test Ad",
                price=1000,
                adtype="rent"
            )
            db.query.return_value.filter.return_value.first.return_value = mock_ad

            result = AdPageCRUD.get_by_id(db, 1)
            
            assert result is not None
            assert result.adpageid == 1
            assert result.title == "Test Ad"
            db.query.assert_called_once()

    def test_get_by_id_failure(self):
        db = MagicMock(spec=Session)
        db.query.return_value.filter.return_value.first.return_value = None

        result = AdPageCRUD.get_by_id(db, 999)
        
        assert result is None
        db.query.assert_called_once()


    def test_create_ad_success(self):
        db = MagicMock(spec=Session)
        ad_data = {
            "adpageid": None,  # Optional field, can be explicitly set to None
            "title": "New Ad",
            "price": 1000,
            "adtype": True,  # Ensure this is a boolean
            "m2": 100,
            "n_floor": 5,
            "floornumber": 3,
            "pet": True,
            "smoking": False,
            "furnished": True,
            "description": "Test description",
            "address": "Test address",
            "gender_choices": 1,
            "ad_date": datetime.now().date(),  # Ensure this is a `date` object
            "userid_fk": 1,
            "neighborhoodid_fk": 1,
            "n_roomid_fk": 1,
        }
        ad_schema = AdPageSchema(**ad_data)
        
        # Mocking database operations
        mock_ad = AdPage(**ad_data)
        db.add.return_value = None
        db.commit.return_value = None
        db.refresh.return_value = None
        
        # Call the method being tested
        result = AdPageCRUD.create(db, ad_schema)
        
        # Assertions to verify functionality
        assert db.add.called
        assert db.commit.called
        assert db.refresh.called
        assert result.title == "New Ad"


    def test_create_ad_failure(self):
        db = MagicMock(spec=Session)
        db.add.side_effect = SQLAlchemyError("Database error")
        
        ad_data = {
            "adpageid": None,  # Optional field, can be explicitly set to None
            "title": "New Ad",
            "price": 1000,
            "adtype": True,  # Ensure this is a boolean
            "m2": 100,
            "n_floor": 5,
            "floornumber": 3,
            "pet": True,
            "smoking": False,
            "furnished": True,
            "description": "Test description",
            "address": "Test address",
            "gender_choices": 1,
            "ad_date": datetime.now().date(),  # Ensure this is a `date` object
            "userid_fk": 1,
            "neighborhoodid_fk": 1,
            "n_roomid_fk": 1,
        }
        ad_schema = AdPageSchema(**ad_data)

        with pytest.raises(SQLAlchemyError):
            AdPageCRUD.create(db, ad_schema)
        
        db.commit.assert_not_called()

    def test_update_ad_success(self):
        db = MagicMock(spec=Session)
        # Mock existing ad
        existing_ad = AdPage(adpageid=1, title="Old Title", price=1000, adtype=True)
        db.query.return_value.filter.return_value.first.return_value = existing_ad

        # Provide update data (ensure all required fields are handled correctly)
        update_data = {
            "adpageid": 1,
            "title": "Updated Title",
            "price": 2000,
            "adtype": True,  # Ensure boolean value for adtype
            "m2": 150,
            "n_floor": 5,
            "floornumber": 3,
            "pet": True,
            "smoking": False,
            "furnished": True,
            "description": "Updated description",
            "address": "Updated address",
            "gender_choices": 2,
            "ad_date": datetime.now().date(),
            "userid_fk": 1,
            "neighborhoodid_fk": 1,
            "n_roomid_fk": 2,
        }
        update_schema = AdPageSchema(**update_data)

        # Call the method being tested
        result = AdPageCRUD.update(db, 1, update_schema)

        # Mocked behavior expectations
        assert db.commit.called
        assert db.refresh.called
        assert result.title == "Updated Title"
        assert result.price == 2000
        assert result.adtype is True

    def test_update_ad_failure(self):
        db = MagicMock(spec=Session)
        # Mock no existing ad found
        db.query.return_value.filter.return_value.first.return_value = None

        # Provide partial update data (not all fields are required in failure scenario)
        update_data = {
            "adpageid": 1,
            "title": "Updated Title",
            "price": 2000,
            "adtype": True,  
            "m2": 150,
            "n_floor": 5,
            "floornumber": 3,
            "pet": True,
            "smoking": False,
            "furnished": True,
            "description": "Updated description",
            "address": "Updated address",
            "gender_choices": 2,
            "ad_date": datetime.now().date(),
            "userid_fk": 1,
            "neighborhoodid_fk": 1,
            "n_roomid_fk": 2,
        }
        update_schema = AdPageSchema(**update_data)


        result = AdPageCRUD.update(db, 999, update_schema)

        # No commit or refresh should occur on failure
        assert not db.commit.called
        assert not db.refresh.called
        assert result is None


    def test_get_userid_by_ad_success(self):
        db = MagicMock(spec=Session)
        mock_userid = MagicMock(userid_fk=42)
        db.query.return_value.filter.return_value.first.return_value = mock_userid

        result = AdPageCRUD.get_userid_by_ad(db, 1)
        
        assert result is not None
        assert result.userid_fk == 42
        db.query.assert_called_once()

    def test_get_userid_by_ad_failure(self):
        db = MagicMock(spec=Session)
        db.query.return_value.filter.return_value.first.return_value = None

        result = AdPageCRUD.get_userid_by_ad(db, 999)
        
        assert result is None
        db.query.assert_called_once()

    def test_delete_ad_success(self):
        db = MagicMock(spec=Session)
        mock_ad = AdPage(adpageid=1, title="Test Ad")
        db.query.return_value.filter.return_value.first.return_value = mock_ad

        result = AdPageCRUD.delete(db, 1)
        
        assert result == {"message": "Advertisement deleted successfully"}
        db.delete.assert_called_once_with(mock_ad)
        db.commit.assert_called_once()

    def test_delete_ad_failure(self):
        db = MagicMock(spec=Session)
        db.query.return_value.filter.return_value.first.return_value = None

        result = AdPageCRUD.delete(db, 999)
        
        assert result is None
        db.delete.assert_not_called()
        db.commit.assert_not_called()

class TestPhotosCRUD:
    def test_create_photos_success(self):
        db = MagicMock(spec=Session)
        photo_urls = ["test1.jpg", "test2.jpg"]
        
        result = PhotosCRUD.create_photos(db, 1, photo_urls)
        
        assert db.bulk_save_objects.called
        assert db.commit.called
        assert len(result) == 2

    def test_create_photos_failure(self):
        db = MagicMock(spec=Session)
        db.bulk_save_objects.side_effect = SQLAlchemyError("Database error")
        photo_urls = ["test1.jpg", "test2.jpg"]
        
        with pytest.raises(SQLAlchemyError):
            PhotosCRUD.create_photos(db, 1, photo_urls)
        
        db.commit.assert_not_called()

    def test_delete_photos_success(self):
        db = MagicMock(spec=Session)
        
        PhotosCRUD.delete_photos(db, 1)
        
        assert db.query.return_value.filter.return_value.delete.called
        assert db.commit.called

    def test_delete_photos_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().delete.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(SQLAlchemyError):
            PhotosCRUD.delete_photos(db, 1)
        
        db.commit.assert_not_called()

        

class TestAdUtilitiesCRUD:
    def test_create_ad_utilities_success(self):
        db = MagicMock(spec=Session)
        utility_ids = [1, 2, 3]
        
        result = AdUtilitiesCRUD.create_ad_utilities(db, 1, utility_ids)
        
        assert db.bulk_save_objects.called
        assert db.commit.called
        assert len(result) == 3

    

    def test_delete_ad_utilities_success(self):
        db = MagicMock(spec=Session)
        
        AdUtilitiesCRUD.delete_ad_utilities(db, 1)
        
        assert db.query.return_value.filter.return_value.delete.called
        assert db.commit.called

    def test_create_ad_utilities_failure(self):
        db = MagicMock(spec=Session)
        db.bulk_save_objects.side_effect = SQLAlchemyError("Database error")
        utility_ids = [1, 2, 3]
        
        with pytest.raises(SQLAlchemyError):
            AdUtilitiesCRUD.create_ad_utilities(db, 1, utility_ids)
        
        db.commit.assert_not_called()

    def test_delete_ad_utilities_failure(self):
        db = MagicMock(spec=Session)
        db.query.return_value.filter.return_value.delete.side_effect = SQLAlchemyError("Database error")
        
        with pytest.raises(SQLAlchemyError):
            AdUtilitiesCRUD.delete_ad_utilities(db, 1)
        
        db.commit.assert_not_called()
