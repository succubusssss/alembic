from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Driver(BaseModel):
    __tablename__ = "driver"

    last_name = Column(String(30), index=True, nullable=False)
    first_name = Column(String(30), index=True, nullable=False)
    patronymic = Column(String(30), index=True, nullable=False)
    passport = Column(String(10), index=True, nullable=False)
    experience = Column(Date, index=True, nullable=False)

    trips = relationship("Trip", cascade="all, delete-orphan", lazy="selectin")