from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AdPage(Base):
    __tablename__ = "ad_page"

    adpageid = Column(Integer, primary_key=True, autoincrement=True)
    userid_fk = Column(Integer)
    neighborhoodid_fk = Column(Integer)
    n_roomid_fk = Column(Integer)
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

#Look up tables for advertisement

class NumberOfRoom(Base):
    __tablename__ = "numberofroom"

    n_roomid = Column(Integer, primary_key=True, autoincrement=True)
    n_room = Column(String(3))

class Neighborhood(Base):
    __tablename__ = "neighborhood"

    neighborhoodid = Column(Integer, primary_key=True, autoincrement=True)
    districtid_fk = Column(Integer, ForeignKey("district.districtid"), nullable=False)
    neighborhood_name = Column(String(40), nullable=False)

    # Relationships
    district = relationship("District", back_populates="neighborhoods")

class District(Base):
    __tablename__ = "district"

    districtid = Column(Integer, primary_key=True, autoincrement=True)
    district_name = Column(String(30), nullable=False)

    # Relationship with Neighborhood
    neighborhoods = relationship("Neighborhood", back_populates="district")
class AdUtilities(Base):
    __tablename__ = 'ad_utilities'

    adpageid = Column(Integer, ForeignKey('ad_page.adpageID'), primary_key=True)
    utilityid = Column(Integer, ForeignKey('utilities.utilityid'), primary_key=True)

    # Relationships
    utility = relationship('Utilities', back_populates='ad_utilities')
    ad_page = relationship('AdPage', back_populates='ad_utilities')


class Utilities(Base):
    __tablename__ = 'utilities'

    utilityid = Column(Integer, primary_key=True, autoincrement=True)
    utility_name = Column(String(20), nullable=False)

    # Relationship to Ad_utilities
    ad_utilities = relationship('AdUtilities', back_populates='utility')