from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from crud.favorites import favoritesCRUD
from models.favorites import Favorites
from models.Advertisement import AdPage, Photos
from models.User import UserPageInfo


class TestFavoritesCRUD:
    def test_get_user_favorites_success(self):
        db = MagicMock(spec=Session)
        
        db.query().join().join().join().join().join().filter().offset().limit().all.return_value = [
            MagicMock(
                adpageid=1,
                adtype="Rent",
                pet=True,
                smoking=False,
                address="Address 1",
                full_name="User 1",
                price=1000,
                title="Ad 1",
                photourl="photo1.jpg",
            ),
            MagicMock(
                adpageid=2,
                adtype="Sale",
                pet=True,
                smoking=True,
                address="Another Address",
                full_name="Another User",
                price=2000,
                title="Another Ad",
                photourl="photo2.jpg",
            ),
        ]

        db.query().filter().count.return_value = 2  # Total count mock

        results, total_count = favoritesCRUD.get_user_favorites(db, user_id=1, limit=10, offset=0)

        # Assertions
        assert total_count == 2
        assert len(results) == 2
        assert results[0]["adpageid"] == 1
        assert results[1]["adpageid"] == 2
        assert results[0]["photos"] == ["photo1.jpg"]
        assert results[1]["photos"] == ["photo2.jpg"]

    def test_get_user_favorites_no_results(self):
        db = MagicMock(spec=Session)
        db.query().join().join().join().join().join().filter().offset().limit().all.return_value = []
        db.query().filter().count.return_value = 0  # No results

        results, total_count = favoritesCRUD.get_user_favorites(db, user_id=1, limit=10, offset=0)

        # Assertions
        assert total_count == 0
        assert len(results) == 0


def test_add_to_favorites_success():
    db = MagicMock(spec=Session)

    mock_favorite = MagicMock(spec=Favorites)
    db.add.return_value = None
    db.commit.return_value = None

    # Inputs
    user_id = 1
    adpage_id = 1

    favoritesCRUD.add_to_favorites(db, user_id, adpage_id)

    # Assertions
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_add_to_favorites_failure():
    db = MagicMock(spec=Session)

    db.add.side_effect = Exception("Database error")
    db.commit.return_value = None

    # Inputs
    user_id = 1
    adpage_id = 1

    try:
        favoritesCRUD.add_to_favorites(db, user_id, adpage_id)
    except Exception as e:
        assert str(e) == "Database error"


def test_remove_from_favorites_success():
    db = MagicMock(spec=Session)

    
    db.query.return_value.filter.return_value.delete.return_value = 1  

    
    favoritesCRUD.remove_from_favorites(db, user_id=1, adpage_id=1)

    
    db.query.assert_called()  
    db.commit.assert_called() 


def test_remove_from_favorites_no_match():
    db = MagicMock(spec=Session)

    db.query.return_value.filter.return_value.delete.return_value = 0

    favoritesCRUD.remove_from_favorites(db, user_id=1, adpage_id=1)

    db.query.assert_called()  
    db.commit.assert_called() 