from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

Base = Base

class UserPageInfo(Base):
    __tablename__ = "user_page_info"

    userid_fk = Column(Integer, ForeignKey('Users.userid'), primary_key=True, index=True)
    departmentid_fk = Column(Integer)
    full_name = Column(String(50))
    date_of_birth = Column(String)
    gender = Column(Boolean)
    smoking = Column(Boolean)
    pet = Column(Boolean)
    ppurl = Column(String)
    about = Column(String(300))
    contact = Column(String(100))
    rh = Column(Boolean)

    # Corrected relationship with User
    users = relationship('Users', back_populates='user_info', uselist=False)

class Users(Base):
    __tablename__ = "Users"

    userid = Column(Integer, primary_key=True, index=True)
    e_mail = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship with AdPage
    ads = relationship('AdPage', back_populates='users')

    # Corrected relationship with UserPageInfo
    user_info = relationship('UserPageInfo', back_populates='users', uselist=False)
