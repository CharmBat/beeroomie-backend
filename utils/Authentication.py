from passlib.context import CryptContext
from schemas.Authentication import AuthResponse
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)



def create_response( user_message: str, error_status: int, error_message: str,token: str = None):
    return AuthResponse(
        token=token,
        user_message=user_message,
        error_status=error_status,
        error_message=error_message
    )