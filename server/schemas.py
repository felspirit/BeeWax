from datetime import datetime
from typing import List

from pydantic import BaseModel


class LocationGeneralDetails(BaseModel):
    location_name: str
    lat: float
    lon: float

    class Config:
        orm_mode = True


class Forecast(BaseModel):
    dt: datetime
    humidity: float
    temp: float
    feels_like: float
    location_id: int

    class Config:
        orm_mode = True


class AverageTempPerDay(BaseModel):
    dt: datetime
    avg_temp: float

    class Config:
        orm_mode = True


class AverageTempForCityPerDay(BaseModel):
    location_name: str
    avg_temp_per_day: List[AverageTempPerDay]

    class Config:
        orm_mode = True


class Point(BaseModel):
    # Point is place and time
    dt: datetime
    location_name: str

    class Config:
        orm_mode = True


class LocationFeelsLike(BaseModel):
    location_name: str
    feels_like: float

    class Config:
        orm_mode = True
