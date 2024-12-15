from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

Base = Base

class OfferModel(Base):
    __tablename__ = 'offers'
    
    offerid = Column(Integer, primary_key=True, index=True)
    offererid_fk = Column(Integer)
    offereeid_fk = Column(Integer, ForeignKey('Users.userid'))
    send_message = Column(String)

    users = relationship('Users', back_populates='offers')