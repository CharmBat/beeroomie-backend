from datetime import timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM
from utils.Authentication import get_password_hash, verify_password, create_token, set_and_send_mail, verify_token_email, verify_token_userid
from fastapi_mail import MessageSchema
from fastapi import status
from unittest.mock import patch

class TestAuthenticationUtils:
        def test_verify_password_success(self):
            plain_password = "testpassword"
            hashed_password = get_password_hash(plain_password)
            assert verify_password(plain_password, hashed_password) is True

        def test_verify_password_failure(self):
            plain_password = "testpassword"
            wrong_password = "wrongpassword"
            hashed_password = get_password_hash(plain_password)
            assert verify_password(wrong_password, hashed_password) is False

        def test_create_token_success(self):
            data = {"email": "test@itu.edu.tr"}
            token = create_token(data)
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            assert decoded_data["email"] == "test@itu.edu.tr"

        def test_create_token_expired(self):
            data = {"email": "test@itu.edu.tr"}
            token = create_token(data, expires_delta=timedelta(seconds=-1))
            try:
                jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                assert False, "Token should be expired"
            except jwt.ExpiredSignatureError:
                assert True

        @patch('fastapi_mail.FastMail.send_message')
        def test_set_and_send_mail_success(self, mock_send):
            mock_send.return_value = None
            email_data = MessageSchema(
                subject="Test Email",
                recipients=["test@itu.edu.tr"],
                body="This is a test email.",
                subtype="html"
            )
            response = set_and_send_mail(email_data)
            assert response.user_message == "An activation mail sent to you email. Please check your email for confirmation."
            assert response.error_status == status.HTTP_201_CREATED

        @patch('fastapi_mail.FastMail.send_message')
        def test_set_and_send_mail_failure(self, mock_send):
            mock_send.side_effect = Exception("Mail sending failed")
            email_data = MessageSchema(
                subject="Test Email",
                recipients=["test@itu.edu.tr"],
                body="This is a test email.",
                subtype="html"
            )
            response = set_and_send_mail(email_data)
            assert response.user_message == "An error occurred while sending the email."
            assert response.error_status == status.HTTP_500_INTERNAL_SERVER_ERROR

        def test_verify_token_email_success(self):
            token = create_token({"email": "test@itu.edu.tr"})
            response = verify_token_email(token)
            assert response.user_message == "Token verified successfully."
            assert response.error_status == status.HTTP_200_OK

        def test_verify_token_email_failure(self):
            invalid_token = "invalid.token.here"
            response = verify_token_email(invalid_token)
            assert response.user_message == "Token verification failed."
            assert response.error_status == status.HTTP_400_BAD_REQUEST

        def test_verify_token_userid_success(self):
            token = create_token({"userid": 0})
            response = verify_token_userid(token)
            assert response.user_message == "Token verified successfully."
            assert response.error_status == status.HTTP_200_OK

        def test_verify_token_userid_failure(self):
            invalid_token = "invalid.token.here"
            response = verify_token_userid(invalid_token)
            assert response.user_message == "Token verification failed."
            assert response.error_status == status.HTTP_400_BAD_REQUEST


            #Send_basic_email test edilmedi async için farklı bir test yapısı gerekiyor
            #create_response edilmedi 

