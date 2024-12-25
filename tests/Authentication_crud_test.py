from sqlalchemy.orm import Session
from models.User import Users
from schemas.Authentication import UserInDB
from unittest.mock import MagicMock, patch
from crud.Authentication import AuthCRUD


class TestAuthCRUD:

    def test_get_user_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=1, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=True)
        db.query().filter(Users.e_mail == "test@itu.edu.tr").first.return_value = user

        result = AuthCRUD.get_user("test@itu.edu.tr", db)
        assert result.e_mail == "test@itu.edu.tr"
        assert result.is_confirmed is True

    def test_get_user_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter(Users.e_mail == "test@itu.edu.tr").first.return_value = None

        result = AuthCRUD.get_user("test@itu.edu.tr", db)
        assert result is None

    def test_add_user_to_db_success(self):
        db = MagicMock(spec=Session)
        AuthCRUD.add_user_to_db("test@itu.edu.tr", "hashedpassword", db)
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_add_user_to_db_failure(self):
        db = MagicMock(spec=Session)
        db.add.side_effect = Exception("Database error")
        with patch('builtins.print') as mocked_print:
            AuthCRUD.add_user_to_db("test@itu.edu.tr", "hashedpassword", db)
            mocked_print.assert_called_with("Database error in add_user_to_db: Database error")

    def test_confirm_user_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=False)
        db.query().filter().first.return_value = user

        result = AuthCRUD.confirm_user("test@itu.edu.tr", db)

        assert result== True

    def test_confirm_user_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        result = AuthCRUD.confirm_user("test@itu.edu.tr", db)
        assert result is False

    def test_delete_user_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=True)
        db.query().filter().first.return_value = user

        AuthCRUD.delete_user(0, db)
        db.commit.assert_called_once()

    def test_delete_user_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        with patch('builtins.print') as mocked_print:
            AuthCRUD.delete_user("nonexistent-user-id", db)
            mocked_print.assert_called_with("No user found with userid nonexistent-user-id.")

    def test_update_user_password_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="oldhashedpassword", is_confirmed=True)
        db.query().filter().first.return_value = user

        AuthCRUD.update_user_password(0, "newhashedpassword", db)
        db.commit.assert_called_once()

    def test_update_user_password_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        with patch('builtins.print') as mocked_print:
            AuthCRUD.update_user_password("nonexistent-user-id", "newhashedpassword", db)
            mocked_print.assert_called_with("No user found with userid nonexistent-user-id.")

    def test_get_userid_from_email_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=True)
        db.query().filter().first.return_value = user

        result = AuthCRUD.get_userid_from_email("test@itu.edu.tr", db)
        assert result == 0

    def test_get_userid_from_email_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        result = AuthCRUD.get_userid_from_email("nonexistent@itu.edu.tr", db)
        assert result is None

    def test_confirm_user_by_email_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=False)
        db.query().filter().first.return_value = user

        AuthCRUD.confirm_user("test@itu.edu.tr", db)
        db.commit.assert_called_once()

    def test_confirm_user_by_email_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        with patch('builtins.print') as mocked_print:
            AuthCRUD.confirm_user("nonexistent@itu.edu.tr", db)
            mocked_print.assert_called_with("No user found with email nonexistent@itu.edu.tr.")

    def test_get_email_from_userid_success(self):
        db = MagicMock(spec=Session)
        user = Users(userid=0, e_mail="test@itu.edu.tr", role=False, hashed_password="hashedpassword", is_confirmed=True)
        db.query().filter().first.return_value = user

        result = AuthCRUD.get_email_from_userid(0, db)
        assert result == "test@itu.edu.tr"

    def test_get_email_from_userid_failure(self):
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None

        result = AuthCRUD.get_email_from_userid("nonexistent-user-id", db)
        assert result is None

