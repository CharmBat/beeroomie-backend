from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

Base = Base

class OfferModel(Base):
    __tablename__ = 'offers'
    
    offerid = Column(Integer, primary_key=True, index=True)
    offererid_fk = Column(Integer, ForeignKey('users.userid'))
    offereeid_fk = Column(Integer, ForeignKey('users.userid'))
    send_message = Column(String)

    offerer = relationship('Users', foreign_keys=[offererid_fk], back_populates='sent_offers')
    offeree = relationship('Users', foreign_keys=[offereeid_fk], back_populates='received_offers')