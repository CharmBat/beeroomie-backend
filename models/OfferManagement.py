from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

Base = Base

class OfferModel(Base):
    __tablename__ = 'offers'
    
    offerid = Column(Integer, primary_key=True, index=True)
    offererid_fk = Column(Integer)
    offereeid_fk = Column(Integer, ForeignKey('ad_page.userid_fk'))
    send_message = Column(String)