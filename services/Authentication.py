from fastapi import Depends, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import verify_password,get_password_hash,send_basic_email,create_response
from schemas.Authentication import TokenData,AuthResponse
from crud.Authentication import get_user, add_user_to_db, confirm_user, delete_user, update_user_password,get_userid_from_email, get_user_from_userid
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES,VERIFICATION_KEY
import asyncio
from fastapi_mail import MessageSchema
from pydantic import EmailStr, parse_obj_as





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

token_blacklist = set()

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def register_user_service(email: str, password: str):
    if get_user(email):
        return create_response(
            user_message="This email is already registered to the system.",
            error_status=status.HTTP_409_CONFLICT,
            system_message="Already registered email"
        )

    verification_token=create_token(data={"email": email}, expires_delta=timedelta(minutes=30),KEY=VERIFICATION_KEY)
    verification_url=f"http://localhost:8000/auth/confirm/{verification_token}"
    hashed_password = get_password_hash(password)
    add_user_to_db(email, hashed_password)
    
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



def set_and_send_mail(email_data):
    
    try:
        

        loop = asyncio.get_event_loop()

        
        
        if loop.is_running():
            task = loop.create_task(send_basic_email(email_data))
            asyncio.ensure_future(task)  
        else:
            asyncio.run(send_basic_email(email_data))
        
        return create_response(user_message="An activation mail sent to you email. Please check your email for confirmation.",error_status=status.HTTP_201_CREATED,system_message="Verification mail sent") 
    
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return create_response(user_message="An error occurred while sending the email.",error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,system_message="An error occurred while sending the email.")
    

def confirm_user_service(token):
    
    token_verification_response=verify_token_email(token,VERIFICATION_KEY)
    if token_verification_response.error_status==status.HTTP_200_OK:
        payload = jwt.decode(token, VERIFICATION_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if confirm_user(email) is None:
            return create_response(user_message="Confirmation failed.",error_status=status.HTTP_400_BAD_REQUEST,system_message="Confirmation failed.")
        return create_response(user_message="User confirmed successfully.",error_status=status.HTTP_201_CREATED,system_message="User confirmed successfully.")
    return token_verification_response

def create_token(data: dict, expires_delta: timedelta, KEY:str = SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = create_response(user_message="Couldn't validate your credentials.",
            error_status=status.HTTP_401_UNAUTHORIZED,
            system_message="Credentials validation failed.")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: int = payload.get("userid")
        if userid is None:
            return credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        return credentials_exception
    user = get_user_from_userid(token_data.userid)
    if user is None:
        return credentials_exception
    return user

def login_service(email: str, password: str) -> AuthResponse:
    # Authenticate user
    user = authenticate_user(email, password)
    if not user:
        return create_response(
            user_message="Login failed. Please check your credentials.",
            error_status=status.HTTP_401_UNAUTHORIZED,
            system_message="Incorrect email or password"
        )
   
    
    # Create access token with expiration
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"userid": user.userid}, expires_delta=access_token_expires,KEY=SECRET_KEY
    )
    
    # Return successful response
    return create_response(token=access_token,
        user_message="Login successful",
        error_status=status.HTTP_200_OK,
        system_message=""
    )

def delete_user_service(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userid = payload.get("userid")
        
    if userid is None:
            return create_response(user_message="UserId not found in token",error_status=status.HTTP_400_BAD_REQUEST,system_message="UserId not found in token")
    try:
        delete_user(userid)
        return create_response(user_message="User deleted successfully.",error_status=status.HTTP_201_CREATED,system_message="User deleted successfully.") 
   
    except Exception as e:
        print(f"Invalid token or confirmation failed: {e}")
        return create_response(user_message="Invalid token or deletion failed.",error_status=status.HTTP_400_BAD_REQUEST,system_message="Invalid token or deletion failed.") 
   



def forgot_password_service(email: str):
    if not get_user(email):
        return create_response(
            user_message="User not found.",
            error_status=status.HTTP_404_NOT_FOUND,
            system_message="User not found."
        )
    reset_token=create_token(data={"email": email}, expires_delta=timedelta(minutes=5),KEY=SECRET_KEY)
    reset_url=f"http://localhost:8000/auth/change-password/{reset_token}"
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

def verify_token_email(token: str,SECRET_KEY:str=SECRET_KEY):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            return create_response(
                user_message="Email not found in token.",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="Email not found in token."
            )
        return create_response(
            user_message="Token verified successfully.",
            error_status=status.HTTP_200_OK,
            system_message=""
        )
    except Exception as e:
        print(f"Token verification failed: {e}")
        return create_response(
            user_message="Token verification failed.",
            error_status=status.HTTP_400_BAD_REQUEST,
            system_message="Token verification failed."
        )
def verify_token_userid(token: str,SECRET_KEY:str=SECRET_KEY):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid = payload.get("userid")
        if userid is None:
            return create_response(
                user_message="Userid not found in token.",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="Userid not found in token."
            )
        return create_response(
            user_message="Token verified successfully.",
            error_status=status.HTTP_200_OK,
            system_message=""
        )
    except Exception as e:
        print(f"Token verification failed: {e}")
        return create_response(
            user_message="Token verification failed.",
            error_status=status.HTTP_400_BAD_REQUEST,
            system_message="Token verification failed."
        )

def change_password_service(token: str, new_password: str):

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
            userid = get_userid_from_email(email)
        except Exception as e:
            print(f"Error retrieving userid from email: {e}")
            return create_response(
                user_message="User not found.",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="Unable to retrieve userid from email."
            )

  
    try:
        hashed_password = get_password_hash(new_password)
        update_user_password(userid, hashed_password)
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




