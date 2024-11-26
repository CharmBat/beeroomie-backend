from fastapi import Depends, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import verify_password,get_password_hash,send_basic_email,create_response
from schemas.Authentication import TokenData,AuthResponse
from crud.Authentication import get_user, add_user_to_db, confirm_user, delete_user
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES,VERIFICATION_KEY
import asyncio
from fastapi_mail import MessageSchema
from pydantic import EmailStr, parse_obj_as





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
            error_message="Already registered email"
        )

    verification_token=create_token(data={"email": email}, expires_delta=timedelta(minutes=30),KEY=VERIFICATION_KEY)
    verification_url=f"http://localhost:8000/auth/confirm/{verification_token}"
    hashed_password = get_password_hash(password)
    add_user_to_db(email, hashed_password)
    return set_and_send_mail(email,verification_url)



def set_and_send_mail(email,verification_url):
    
    try:
        validated_email = parse_obj_as(EmailStr, email)
    except Exception as e:
        return create_response(user_message="Invalid email address.",error_status=status.HTTP_400_BAD_REQUEST,error_message="Invalid email address.")

    try:
        email_data = MessageSchema(
    subject="Kayıt İşlemi Başarılı!",
    recipients=[validated_email],  # Note: `recipients` should be a list of email strings
    body=f"""
    <html>
        <body>
            <h1>Merhaba!</h1>
            <p>Aramıza hoş geldiniz! Lütfen kayıt işlemini tamamlamak için bu mesajı dikkate alın.{verification_url}</p>
        </body>
    </html>
    """,
    subtype="html"
)

        loop = asyncio.get_event_loop()

        
        
        if loop.is_running():
            task = loop.create_task(send_basic_email(email_data))
            asyncio.ensure_future(task)  
        else:
            asyncio.run(send_basic_email(email_data))
        
        return create_response(user_message="An activation mail sent to you email. Please check your email for confirmation.",error_status=status.HTTP_201_CREATED,error_message="Verification mail sent") 
    
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return create_response(user_message="An error occurred while sending the email.",error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,error_message="An error occurred while sending the email.")
    

def confirm_user_service(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userid = payload.get("userid")
        
    if userid is None:
            raise ValueError("UserID not found in token")
    try:
        confirm_user(userid)
        return create_response(user_message="User confirmed successfully.",error_status=status.HTTP_201_CREATED,error_message="User confirmed successfully.") 
   
    except Exception as e:
        print(f"Invalid token or confirmation failed: {e}")
        return create_response(user_message="Invalid token or confirmation failed.",error_status=status.HTTP_400_BAD_REQUEST,error_message="Invalid token or confirmation failed.") 
   


def create_token(data: dict, expires_delta: timedelta, KEY:str = SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = create_response(user_message="Couldn't validate your credentials.",
            error_status=status.HTTP_401_UNAUTHORIZED,
            error_message="Credentials validation failed.")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: int = payload.get("sub")
        if userid is None:
            return credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        return credentials_exception
    user = get_user(token_data.userid)
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
            error_message="Incorrect email or password"
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
        error_message=""
    )

def delete_user_service(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userid = payload.get("userid")
        
    if userid is None:
            raise ValueError("UserId not found in token")
    try:
        delete_user(userid)
        return create_response(user_message="User deleted successfully.",error_status=status.HTTP_201_CREATED,error_message="User deleted successfully.") 
   
    except Exception as e:
        print(f"Invalid token or confirmation failed: {e}")
        return create_response(user_message="Invalid token or deletion failed.",error_status=status.HTTP_400_BAD_REQUEST,error_message="Invalid token or deletion failed.") 
   




