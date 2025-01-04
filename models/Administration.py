from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

Base = Base


class Blacklist(Base):
    __tablename__ = "blacklist"

    e_mail = Column(String(60), primary_key=True)
    ban_date = Column(Date, nullable=False)
    ban_reason = Column(String(150), nullable=False)



class Reports(Base):
    __tablename__ = "reports"

    reportid = Column(Integer, primary_key=True, autoincrement=True)
    reporter = Column(Integer, ForeignKey('users.userid', ondelete="CASCADE"), nullable=False)
    reportee = Column(Integer, ForeignKey('users.userid', ondelete="CASCADE"), nullable=False)
    description = Column(String(140), nullable=False)
    report_date = Column(Date, nullable=False)

    # Relationships to User
    reporter_user = relationship(
        "Users",
        foreign_keys=[reporter],
        back_populates="reports_as_reporter",
        cascade="all, delete"
    )
    reportee_user = relationship(
        "Users",
        foreign_keys=[reportee],
        back_populates="reports_as_reportee",
        cascade="all, delete"
    )