from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

Base = Base

class Favorites(Base):
    __tablename__ = "favorites"

    # Columns
    userid_fk = Column(Integer, ForeignKey('users.userid', ondelete="CASCADE"), primary_key=True)
    adpageid_fk = Column(Integer, ForeignKey('ad_page.adpageid', ondelete="CASCADE"), primary_key=True)

    # Relationships
    user = relationship("Users", back_populates="favorites")
    ad_page = relationship("AdPage", back_populates="favorited_by")