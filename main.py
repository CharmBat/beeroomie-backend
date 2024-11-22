from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext   
from jose import JWTError, jwt
from typing import Optional
from dotenv import load_dotenv

from routers import Authentication
app = FastAPI()

app.include_router(Authentication.router)
# Configuration
load_dotenv()






