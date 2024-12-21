from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi_mail import MessageSchema
from config import MAIL_USERNAME, MAIL_FROM, MAIL_PORT, MAIL_PASSWORD, MAIL_SERVER
from config import SECRET_KEY, ALGORITHM
from fastapi_mail import ConnectionConfig, FastMail
from schemas.Authentication import AuthResponse
import asyncio
from jose import jwt
from fastapi import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)





def create_token(data: dict, KEY: str = SECRET_KEY, expires_delta: timedelta = timedelta(minutes=0)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt




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
    


async def send_basic_email(email_data: MessageSchema):

    conf = ConnectionConfig(
    MAIL_USERNAME= MAIL_USERNAME,      
    MAIL_PASSWORD=MAIL_PASSWORD,       
    MAIL_FROM=MAIL_FROM,           
    MAIL_PORT=MAIL_PORT,                            
    MAIL_SERVER=MAIL_SERVER, 
                                        
    MAIL_FROM_NAME="beeromie",                     
    MAIL_STARTTLS=False,                           
    MAIL_SSL_TLS=True,                            
    USE_CREDENTIALS=True,                           
    VALIDATE_CERTS=False                           
)
    fm = FastMail(conf)
    await fm.send_message(email_data) 

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


def create_response( user_message: str, error_status: int, system_message: str,token: str = None):
    return AuthResponse(
        token=token,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

