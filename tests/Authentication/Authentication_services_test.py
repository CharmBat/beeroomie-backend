from unittest.mock import patch, MagicMock

from ..conftest import Base, engine, client
from config import VERIFICATION_KEY, SECRET_KEY
from jose import jwt
from datetime import datetime, timedelta
from services.Authentication import AuthenticationService
from models.Administration import Blacklist
from schemas.Authentication import MeResponse


def create_test_token(data: dict, expire_minutes: int = 15, KEY: str =SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm="HS256")
    return encoded_jwt

class TestAuthenticationServices:
    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(bind=engine)

    

    @patch('services.Authentication.AuthenticationService.authenticate_user')
    def test_login_success(self, mock_auth):
        mock_auth.return_value = MagicMock(
            userid=0,
            role=False
        )
        
        response = client.post(
            "/auth/login",
            data={
                "grant_type": "password",
                "username": "test@itu.edu.tr",
                "password": "testpass",
                "scope": "",
                "client_id": "string",
                "client_secret": "string"
            }
        )
        print(response.json())
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["user_message"] == "Login successful"

    @patch('services.Authentication.AuthenticationService.authenticate_user')
    def test_login_failure(self, mock_auth):
        mock_auth.return_value = False
        
        response = client.post(
            "/auth/login",
            data={
                "grant_type": "password",
                "username": "wrong@itu.edu.tr",
                "password": "wrongpass",
                "scope": "",
                "client_id": "string",
                "client_secret": "string"
            }
        )
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 401
        assert "Login failed" in response.json()["user_message"]

    @patch('sqlalchemy.orm.Session.query')
    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.AuthCRUD.add_user_to_db')
    @patch('services.Authentication.set_and_send_mail')
    def test_register_user(self, mock_mail, mock_add_user, mock_get_user, mock_query):
        mock_query.return_value.filter.return_value.first.return_value = None
        mock_get_user.return_value = None
        mock_mail.return_value = {
            "user_message": "Registration successful",
            "error_status": 200,
            "system_message": ""
        }
        
        response = client.post(
            "/auth/register",
            json={"email": "new@itu.edu.tr", "password": "newpass"}
        )
        
        assert response.status_code == 200
        assert "Registration successful" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.get_user')
    def test_register_existing_user(self, mock_get_user):
        mock_get_user.return_value = MagicMock()
    
        response = client.post(
            "/auth/register",
            json={"email": "existing@itu.edu.tr", "password": "password"}
        )
    
        assert response.status_code == 200
        assert response.json()["error_status"] == 409
        assert "Bu email sisteme zaten kayıtlı." in response.json()["user_message"]


    @patch('services.Authentication.AuthCRUD.confirm_user')
    def test_confirm_user_success(self, mock_confirm):
        mock_confirm.return_value = True
        test_token = create_test_token({"email": "test@itu.edu.tr"}, expire_minutes=0, KEY=VERIFICATION_KEY)
        
        response = client.get(f"/auth/confirm/{test_token}")
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 201
        assert "User confirmed successfully" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.confirm_user')
    def test_confirm_user_failure(self, mock_confirm):
        mock_confirm.return_value = False
        test_token = create_test_token({"email": "wrongtest@itu.edu.tr"}, expire_minutes=0, KEY=VERIFICATION_KEY)
        
        response = client.get(f"/auth/confirm/{test_token}")
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 400
        assert "Confirmation failed." in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.set_and_send_mail')
    def test_forgot_password(self, mock_mail, mock_get_user):
        mock_get_user.return_value = MagicMock()
        mock_mail.return_value = {
            "user_message": "Password reset link sent",
            "error_status": 200,
            "system_message": ""
        }
        
        response = client.post(
            "/auth/forgot-password/",
            params={"email": "test@itu.edu.tr"}
        )
        
        assert response.status_code == 200
        assert "Password reset link sent" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.set_and_send_mail')
    def test_forgot_password_user_not_found(self, mock_mail, mock_get_user):
        mock_get_user.return_value = None
        
        response = client.post(
            "/auth/forgot-password/",
            params={"email": "nonexistent@itu.edu.tr"}
        )
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 404
        assert "User not found" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.update_user_password')
    def test_change_password(self, mock_update):
        test_token = create_test_token({"userid": 0, "email": "test@itu.edu.tr"}, expire_minutes=15, KEY=SECRET_KEY)
        
        response = client.get(
            f"/auth/change-password/{test_token}",
            params={"new_password": "newpassword"}
        )
        
        assert response.status_code == 200
        assert "Password changed successfully" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.update_user_password')
    def test_change_password_failure(self, mock_update):
        mock_update.side_effect = Exception("Password change failed")
        test_token = create_test_token({"userid": 0, "email": "test@itu.edu.tr"}, expire_minutes=15, KEY=SECRET_KEY)
        
        response = client.get(
            f"/auth/change-password/{test_token}",
            params={"new_password": "newpassword"}
        )
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 500
        assert "Failed to change password." in response.json()["user_message"]

    def test_logout(self):
        test_token = create_test_token({"userid": 0})
        
        response = client.post(f"/auth/logout/{test_token}")
        
        assert response.status_code == 200
        assert response.json()["user_message"] == "Logout successful"

    def test_invalid_token(self):
        invalid_token = "invalid.token.here"
        
        response = client.get(f"/auth/confirm/{invalid_token}")
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 400
        assert "Token verification failed." in response.json()["user_message"]
    @patch('services.Authentication.AuthCRUD.confirm_user')
    @patch('services.Authentication.verify_token_email')
    def test_confirm_user_service_success(self, mock_verify_token, mock_confirm):
        mock_verify_token.return_value = MagicMock(
            error_status=200
        )
        mock_confirm.return_value = True
        test_token = create_test_token({"email": "email@itu.edu.tr"}, expire_minutes=0, KEY=VERIFICATION_KEY)
        
        response = client.get(f"/auth/confirm/{test_token}")
        
        assert response.status_code == 200
        assert response.json()["error_status"] == 201
        assert "User confirmed successfully" in response.json()["user_message"]

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.verify_password')
    def test_authenticate_user_success(self, mock_verify_password, mock_get_user):
        mock_get_user.return_value = MagicMock(
            email="test@itu.edu.tr",
            hashed_password="hashedpassword"
        )
        mock_verify_password.return_value = True
        
        result = AuthenticationService.authenticate_user("test@itu.edu.tr", "testpass", MagicMock())
        
        assert result is not False
        assert result.email == "test@itu.edu.tr"

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.verify_password')
    def test_authenticate_user_failure_user_not_found(self, mock_verify_password, mock_get_user):
        mock_get_user.return_value = None
        
        result = AuthenticationService.authenticate_user("wrong@itu.edu.tr", "testpass", MagicMock())
        
        assert result is False

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.verify_password')
    def test_authenticate_user_failure_wrong_password(self, mock_verify_password, mock_get_user):
        mock_get_user.return_value = MagicMock(
            email="test@itu.edu.tr",
            hashed_password="hashedpassword"
        )
        mock_verify_password.return_value = False
        
        result = AuthenticationService.authenticate_user("test@itu.edu.tr", "wrongpass", MagicMock())
        
        assert result is False

    @patch('services.Authentication.AuthCRUD.get_user')
    @patch('services.Authentication.AuthCRUD.add_user_to_db')
    @patch('services.Authentication.set_and_send_mail')
    @patch('sqlalchemy.orm.Session.query')  
    def test_register_user_blacklisted_email(self, mock_query, mock_mail, mock_add_user, mock_get_user):
        mock_blacklist_entry = MagicMock(e_mail="blacklisted@itu.edu.tr")
        mock_query.return_value.filter.return_value.first.return_value = mock_blacklist_entry
        mock_get_user.return_value = None
    
        response = client.post(
            "/auth/register",
            json={"email": "blacklisted@itu.edu.tr", "password": "password123"}
        )
    
        assert response.status_code == 200
        assert response.json()["error_status"] == 403
        assert "Your email is blacklisted" in response.json()["user_message"]
    
        mock_add_user.assert_not_called()
        mock_mail.assert_not_called()

