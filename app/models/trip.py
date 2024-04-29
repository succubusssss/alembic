from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.models.base import BaseModel

class Trip(BaseModel):
    __tablename__ = "trip"

    driver_id = Column(Integer, ForeignKey("driver.id"))
    departure_time  = Column(DateTime, index=True, nullable=False)

    driver = relationship("Driver", back_populates="trips")