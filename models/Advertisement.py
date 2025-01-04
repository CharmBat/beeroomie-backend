from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

Base = Base

class AdPage(Base):
    __tablename__ = "ad_page"

    adpageid = Column(Integer, primary_key=True, autoincrement=True)
    userid_fk = Column(Integer, ForeignKey('users.userid'))  # Fixed ForeignKey reference
    neighborhoodid_fk = Column(Integer, ForeignKey('neighborhood.neighborhoodid'))
    n_roomid_fk = Column(Integer, ForeignKey('numberofroom.n_roomid'))
    title = Column(String(100))
    price = Column(Integer)
    adtype = Column(Boolean)
    m2 = Column(Integer)
    n_floor = Column(Integer)
    floornumber = Column(Integer)
    pet = Column(Boolean)
    smoking = Column(Boolean)
    furnished = Column(Boolean)
    description = Column(String(300))
    address = Column(String(300))
    gender_choices = Column(Integer)
    ad_date = Column(Date)

    # Relationships
    users = relationship('Users', back_populates='ads')
    neighborhood = relationship('Neighborhood', back_populates='ads')
    room_type = relationship('NumberOfRoom', back_populates='ads')
    photos = relationship('Photos', back_populates='ad_page', cascade="all, delete")
    ad_utilities = relationship('AdUtilities', back_populates='ad_page', cascade="all, delete")
    favorited_by = relationship('Favorites', back_populates='ad_page', cascade="all, delete")

class NumberOfRoom(Base):
    __tablename__ = "numberofroom"

    n_roomid = Column(Integer, primary_key=True, autoincrement=True)
    n_room = Column(String(3))

    # Relationship with AdPage
    ads = relationship('AdPage', back_populates='room_type')

class Neighborhood(Base):
    __tablename__ = "neighborhood"

    neighborhoodid = Column(Integer, primary_key=True, autoincrement=True)
    districtid_fk = Column(Integer, ForeignKey("district.districtid", ondelete='CASCADE'), nullable=False)
    neighborhood_name = Column(String(40), nullable=False)

    # Relationships
    district = relationship("District", back_populates="neighborhoods")
    ads = relationship('AdPage', back_populates='neighborhood')

class District(Base):
    __tablename__ = "district"

    districtid = Column(Integer, primary_key=True, autoincrement=True)
    district_name = Column(String(30), nullable=False)

    # Relationship with Neighborhood
    neighborhoods = relationship("Neighborhood", back_populates="district", cascade="all, delete")

class AdUtilities(Base):
    __tablename__ = 'ad_utilities'

    adpageid_fk = Column(Integer, ForeignKey('ad_page.adpageid', ondelete='CASCADE'), primary_key=True)
    utilityid_fk = Column(Integer, ForeignKey('utilities.utilityid', ondelete='CASCADE'), primary_key=True)

    # Relationships
    utility = relationship('Utilities', back_populates='ad_utilities')
    ad_page = relationship('AdPage', back_populates='ad_utilities')

class Utilities(Base):
    __tablename__ = 'utilities'

    utilityid = Column(Integer, primary_key=True, autoincrement=True)
    utility_name = Column(String(20), nullable=False)

    # Relationship to Ad_utilities
    ad_utilities = relationship('AdUtilities', back_populates='utility')

class Photos(Base):
    __tablename__ = 'photos'

    photoid = Column(Integer, primary_key=True, autoincrement=True)
    adpageid_fk = Column(Integer, ForeignKey('ad_page.adpageid', ondelete='CASCADE'))
    photourl = Column(String(200), nullable=False)

    # Relationships
    ad_page = relationship('AdPage', back_populates='photos')





