from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from .database import Base


class LocationGeneralDetails(Base):
    __tablename__ = "locations_general_details"

    id = Column(Integer, primary_key=True)
    location_name = Column(String, unique=True)
    lat = Column(Float)
    lon = Column(Float)

    forecasts = relationship("Forecast", back_populates="location")


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime)
    humidity = Column(Float)
    temp = Column(Float)
    feels_like = Column(Float)
    location_id = Column(Integer, ForeignKey(
        "locations_general_details.id"), index=True)

    location = relationship("LocationGeneralDetails",
                            back_populates="forecasts")

    __table_args__ = (UniqueConstraint("dt", "location_id"),)
