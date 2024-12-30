from sqlalchemy.orm import Session
from models.User import UserPageInfo
from schemas.UserPageInfo import UserPageInfoSchema
from unittest.mock import MagicMock, patch
from crud.UserPageInfo import UserPageInfoCRUD
from datetime import date

class TestUserPageInfoCRUD:
    def test_create_success(self):
        db = MagicMock(spec=Session)
        user_info = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        result = UserPageInfoCRUD.create(db, user_info)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        
    def test_create_failure_db_error(self):
        db = MagicMock(spec=Session)
        db.add.side_effect = Exception("Database error")
        user_info = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        try:
            UserPageInfoCRUD.create(db, user_info)
            assert False, "Expected an exception but none was raised"
        except Exception as e:
            assert str(e) == "Database error"
            
    def test_get_by_userid_success(self):
        db = MagicMock(spec=Session)
        user_info = UserPageInfo(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        db.query().filter().first.return_value = user_info
        
        result = UserPageInfoCRUD.get_by_userid(db, 1)
        assert result.userid_fk == 1
        assert result.full_name == "Test Kullanıcı"
        
    def test_get_by_userid_not_found(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None
        
        result = UserPageInfoCRUD.get_by_userid(db, 999)
        assert result is None
        
    def test_get_by_userid_failure_db_error(self):
        db = MagicMock(spec=Session)
        db.query.side_effect = Exception("Database error")
        
        try:
            UserPageInfoCRUD.get_by_userid(db, 1)
            assert False, "Expected an exception but none was raised"
        except Exception as e:
            assert str(e) == "Database error"
            
    def test_update_success(self):
        db = MagicMock(spec=Session)
        existing_user_info = UserPageInfo(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Eski İsim",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        db.query().filter().first.return_value = existing_user_info
        
        update_data = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Yeni İsim",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        result = UserPageInfoCRUD.update(db, 1, update_data)
        db.commit.assert_called_once()
        
    def test_update_not_found(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None
        
        update_data = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Yeni İsim",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        result = UserPageInfoCRUD.update(db, 999, update_data)
        assert result is None
        
    def test_update_failure_db_error(self):
        db = MagicMock(spec=Session)
        existing_user_info = UserPageInfo(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Eski İsim",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        db.query().filter().first.return_value = existing_user_info
        db.commit.side_effect = Exception("Database error")
        
        update_data = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Yeni İsim",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        try:
            UserPageInfoCRUD.update(db, 1, update_data)
            assert False, "Expected an exception but none was raised"
        except Exception as e:
            assert str(e) == "Database error"

    def test_get_ppurl_by_userid_success(self):
        db = MagicMock(spec=Session)
        # Create a mock result with ppurl
        mock_result = MagicMock()
        mock_result.ppurl = "test.jpg"
        
        # Set up the mock chain
        db.query().filter().first.return_value = mock_result
        
        result = UserPageInfoCRUD.get_ppurl_by_userid(db, 1)
        assert result == "test.jpg"

    def test_get_ppurl_by_userid_failure(self):
        db = MagicMock(spec=Session)
        # Set up the mock chain to return None
        db.query().filter().first.return_value = None
        
        result = UserPageInfoCRUD.get_ppurl_by_userid(db, 999)
        assert result is None

    def test_set_rh_status_success(self):
        db = MagicMock(spec=Session)
        user_info = UserPageInfo(
            userid_fk=1,
            rh=False
        )
        db.query().filter().first.return_value = user_info
        
        result = UserPageInfoCRUD.set_rh_status(db, 1, True)
        assert result.rh is True
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    def test_set_rh_status_failure_user_not_found(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None
        
        result = UserPageInfoCRUD.set_rh_status(db, 999, True)
        assert result is None

    def test_set_rh_status_failure_db_error(self):
        db = MagicMock(spec=Session)
        user_info = UserPageInfo(
            userid_fk=1,
            rh=False
        )
        db.query().filter().first.return_value = user_info
        db.commit.side_effect = Exception("Database error")
        
        try:
            UserPageInfoCRUD.set_rh_status(db, 1, True)
            assert False, "Expected an exception but none was raised"
        except Exception as e:
            assert str(e) == "Database error"