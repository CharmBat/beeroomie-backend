from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    userid = Column(Integer, primary_key=True, index=True)
    e_mail = Column(String, unique=True, index=True)
    hashed_password = Column(String)