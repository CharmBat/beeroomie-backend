from fastapi import Depends, status
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import get_password_hash,create_response,create_token,set_and_send_mail,verify_token_email,verify_password
from schemas.Authentication import AuthResponse, TokenData
from crud.Authentication import AuthCRUD
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES, VERIFICATION_KEY, FRONTEND_URL_PREFIX
from fastapi_mail import MessageSchema
from pydantic import EmailStr, parse_obj_as
from crud.UserPageInfo import UserPageInfoCRUD
from services.PhotoHandle import PhotoHandleService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_blacklist = set()

class AuthenticationService:

    @staticmethod
    def authenticate_user(email: str, password: str,db):
        user = AuthCRUD.get_user(email,db)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user


    @staticmethod
    def register_user_service(email: str, password: str,db):
        if AuthCRUD.get_user(email,db):
            return create_response(
                user_message="This email is already registered to the system.",
                error_status=status.HTTP_409_CONFLICT,
                system_message="Already registered email"
            )

        verification_token=create_token(data={"email": email}, KEY=VERIFICATION_KEY)
        verification_url=f"{FRONTEND_URL_PREFIX}/confirm-email/{verification_token}"
        hashed_password = get_password_hash(password)
        AuthCRUD.add_user_to_db(email, hashed_password,db)
        
        email_data = MessageSchema(
        subject="Kayıt İşlemi Başarılı!",
        recipients=[parse_obj_as(EmailStr, email)],  # Note: `recipients` should be a list of email strings
        body=f"""
        <html>
            <body>
                <h1>Merhaba!</h1>
                <p>Aramıza hoş geldiniz! Lütfen kayıt işlemini tamamlamak için bu mesajı dikkate alın.</p>
                <br>
                <p>{verification_url}</p>
            </body>
        </html>
        """,
        subtype="html"
    )
        return set_and_send_mail(email_data)

    @staticmethod
    def confirm_user_service(token,db):
        result=AuthCRUD.confirm_user("email@itu.edu.tr",db)
        token_verification_response=verify_token_email(token,VERIFICATION_KEY)
        if token_verification_response.error_status==status.HTTP_200_OK:
            payload = jwt.decode(token, VERIFICATION_KEY, algorithms=[ALGORITHM])
            email = payload.get("email")
            if AuthCRUD.confirm_user(email,db) is False:
                return create_response(user_message="Confirmation failed.",error_status=status.HTTP_400_BAD_REQUEST,system_message="Confirmation failed.")
            return create_response(user_message="User confirmed successfully.",error_status=status.HTTP_201_CREATED,system_message="User confirmed successfully.")
        return token_verification_response



    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = create_response(user_message="Couldn't validate your credentials.",
                error_status=status.HTTP_401_UNAUTHORIZED,
                system_message="Credentials validation failed.")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            userid: str = payload.get("userid")
            role: bool = payload.get("role")

            if userid is None:
                return credentials_exception
        except JWTError:
            return credentials_exception
        user = TokenData(userid=userid,role=role)
        if user is None:
            return credentials_exception
        return user

    @staticmethod
    def login_service(email: str, password: str,db) -> AuthResponse:
        # Authenticate user
        user = AuthenticationService.authenticate_user(email, password,db)
        if not user:
            return create_response(
                user_message="Login failed. Please check your credentials. Be sure your account is verified!!!",
                error_status=status.HTTP_401_UNAUTHORIZED,
                system_message="Incorrect email or password"
            )
    
        
        # Create access token with expiration
        access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        access_token = create_token(
            data={"userid": user.userid, "role": user.role}, expires_delta=access_token_expires, KEY=SECRET_KEY
        )
        
        # Return successful response
        return create_response(access_token=access_token,
            user_message="Login successful",
            error_status=status.HTTP_200_OK,
            system_message=""
        )

    # @staticmethod
    # def delete_user_service(userid,db):
    #     if not AuthCRUD.get_user(userid,db):
    #         return create_response(user_message="User not found.",error_status=status.HTTP_404_NOT_FOUND,system_message="User not found.")

    #     try:
    #         AuthCRUD.delete_user(userid,db)
    #         deleted_user_info=UserPageInfoCRUD.get_by_userid(userid,db)
    #         if deleted_user_info.ppurl:
    #             PhotoHandleService.photo_delete_service(deleted_user_info.ppurl)
    #         return create_response(user_message="User deleted successfully.",error_status=status.HTTP_201_CREATED,system_message="User deleted successfully.") 
    
    #     except Exception as e:
    #         print(f"Invalid userid or confirmation failed: {e}")
    #         return create_response(user_message="Invalid userid or deletion failed.",error_status=status.HTTP_400_BAD_REQUEST,system_message="Invalid userid or deletion failed.") 
    


    @staticmethod
    def forgot_password_service(email: str,db):
        if not AuthCRUD.get_user(email,db):
            return create_response(
                user_message="User not found.",
                error_status=status.HTTP_404_NOT_FOUND,
                system_message="User not found."
            )
        reset_token=create_token(data={"email": email}, expires_delta=timedelta(minutes=5),KEY=SECRET_KEY)
        reset_url=f"{FRONTEND_URL_PREFIX}/reset-password/{reset_token}"
        email_data = MessageSchema(
        subject="Şifre Sıfırlama",
        recipients=[parse_obj_as(EmailStr, email)],  # Note: `recipients` should be a list of email strings
        body=f"""
        <html>
            <body>
                <h1>Merhaba!</h1>
                <p>Eğer şifrenizi sıfırlamak istiyorsanız linke tıklayın.</p>
                <br>
                <p>{reset_url}</p>
            </body>
        </html>
        """,
        subtype="html"
    )
        set_and_send_mail(email_data)
        return create_response(
            user_message="Password reset link sent to your email. Please check your email for confirmation.",
            error_status=status.HTTP_200_OK,
            system_message="Password reset link sent."
        )


    @staticmethod
    def change_password_service(token: str, new_password: str,db):

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception as e:
            print(f"Token decoding failed: {e}")
            return create_response(
                user_message="Invalid or expired token.",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="Token decoding failed."
            )

        
        userid = payload.get("userid")
        if not userid:
            
            email = payload.get("email")
            if not email:
                return create_response(
                    user_message="User information missing in token.",
                    error_status=status.HTTP_400_BAD_REQUEST,
                    system_message="No userid or email in token."
                )
            try:
                userid = AuthCRUD.get_userid_from_email(email,db)
            except Exception as e:
                print(f"Error retrieving userid from email: {e}")
                return create_response(
                    user_message="User not found.",
                    error_status=status.HTTP_400_BAD_REQUEST,
                    system_message="Unable to retrieve userid from email."
                )

    
        try:
            hashed_password = get_password_hash(new_password)
            AuthCRUD.update_user_password(userid, hashed_password,db)
            return create_response(
                user_message="Password changed successfully.",
                error_status=status.HTTP_200_OK,
                system_message="Password changed successfully."
            )
        except Exception as e:
            print(f"Password change failed: {e}")
            return create_response(
                user_message="Failed to change password.",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message="Password update operation failed."
            )

    @staticmethod
    def logout_service(token: str) -> dict:
        print(f"Token received: {token}")  

        if not token:  
            return AuthResponse(
                token=None,
                user_message="No token provided",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="No token provided"
            )
        
        if token not in token_blacklist:
            token_blacklist.add(token)

        return AuthResponse(
            token=None,
            user_message="Logout successful",
            error_status=status.HTTP_200_OK,
            system_message=""
        )




