from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from main import app
from db.database import get_db
from schemas.Authentication import TokenData
from services.Authentication import AuthenticationService

class Base(DeclarativeBase):
    pass

# Test database setup
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return TokenData(userid=333, role=False)

# Setup test client with dependency overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[AuthenticationService.get_current_user] = override_get_current_user
