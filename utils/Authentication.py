from passlib.context import CryptContext

from fastapi_mail import MessageSchema
from config import MAIL_USERNAME, MAIL_FROM, MAIL_PORT, MAIL_PASSWORD, MAIL_SERVER
from fastapi_mail import ConnectionConfig, FastMail
from schemas.Authentication import AuthResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


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

def create_response( user_message: str, error_status: int, system_message: str,token: str = None):
    return AuthResponse(
        token=token,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

