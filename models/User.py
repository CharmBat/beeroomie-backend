from sqlalchemy import Boolean, Column, Integer, String, Date,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

Base = Base

class UserPageInfo(Base):
    __tablename__ = "user_page_info"

    userid_fk = Column(Integer, ForeignKey('users.userid'), primary_key=True, index=True)
    departmentid_fk = Column(Integer, ForeignKey("department.departmentid"))
    full_name = Column(String(50))
    date_of_birth = Column(Date)
    gender = Column(Boolean)
    smoking = Column(Boolean)
    pet = Column(Boolean)
    ppurl = Column(String)
    about = Column(String(300))
    contact = Column(String(100))
    rh = Column(Boolean)

    # Corrected relationship with User
    users = relationship('Users', back_populates='user_info', uselist=False)
    department = relationship('Department', back_populates='user_page_info')
    blacklist = relationship("Blacklist", back_populates="user", uselist=False)

class Users(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True)
    e_mail = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_confirmed = Column(Boolean, default=False)
    role=Column(Boolean,default=False)

    # Relationship with AdPage
    ads = relationship('AdPage', back_populates='users', cascade="all, delete")

    # Corrected relationship with UserPageInfo
    user_info = relationship('UserPageInfo', back_populates='users', uselist=False, cascade="all, delete")

        # Offers relationships
    sent_offers = relationship(
        'OfferModel',
        foreign_keys='OfferModel.offererid_fk',
        back_populates='offerer',
        cascade="all, delete"
    )
    received_offers = relationship(
        'OfferModel',
        foreign_keys='OfferModel.offereeid_fk',
        back_populates='offeree',
        cascade="all, delete"
    )

class Department(Base):
    __tablename__ = "department"

    departmentid = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(150), nullable=False)

    # Relationship with UserPageInfo
    user_page_info = relationship('UserPageInfo', back_populates='department', cascade="all, delete")