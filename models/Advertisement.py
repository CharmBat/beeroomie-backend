from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AdPage(Base):
    __tablename__ = "Ad_page"

    adpageID = Column(Integer, primary_key=True)
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
    gender_choice = Column(Integer)
    ad_date = Column(Date)