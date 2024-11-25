from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import verify_password,get_password_hash,send_basic_email
from schemas.Authentication import TokenData
from schemas.Authentication import AuthResponse
from crud.Authentication import get_user, add_user_to_db
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES
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

    
    #hashed_password = get_password_hash(password)
    #add_user_to_db(email, hashed_password)
    return set_and_send_mail(email)



def set_and_send_mail(email):
    
    try:
        validated_email = parse_obj_as(EmailStr, email)
    except Exception as e:
        return {"message": f"Invalid email format: {e}"}

    try:
        email_data = MessageSchema(
    subject="Kayıt İşlemi Başarılı!",
    recipients=[validated_email],  # Note: `recipients` should be a list of email strings
    body="""
    <html>
        <body>
            <h1>Merhaba!</h1>
            <p>Aramıza hoş geldiniz! Lütfen kayıt işlemini tamamlamak için bu mesajı dikkate alın.</p>
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
        
        return {"message": "Registration successful, an email has been sent to your inbox."}
    
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return {"message": "Mail sending failed, please try again later."}
    



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: int = payload.get("sub")
        if userid is None:
            raise credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.userid)
    if user is None:
        raise credentials_exception
    return user

def login_service(email: str, password: str) -> AuthResponse:
    # Authenticate user
    user = authenticate_user(email, password)
    if not user:
        return AuthResponse(
            token=None,
            user_message="Login failed. Please check your credentials.",
            error_status=status.HTTP_401_UNAUTHORIZED,
            error_message="Incorrect email or password"
        )
    
    # Create access token with expiration
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.userid}, expires_delta=access_token_expires
    )
    
    # Return successful response
    return AuthResponse(
        token=access_token,
        user_message="Login successful",
        error_status=status.HTTP_200_OK,
        error_message=""
    )