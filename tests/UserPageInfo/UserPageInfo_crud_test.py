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