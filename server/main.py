from enum import Enum
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import openweather, schemas
from .db_handler import crud, models
from .db_handler.database import SessionLocal, engine

LOCATIONS_TO_GEOCODE = ["Jerusalem,IL", "Haifa,IL", "Tel Aviv,IL",
                        "Eilat,IL", "Tiberias,IL"]


class OrderDir(str, Enum):
    ascending = "asc"
    descending = "desc"


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return "Hello!"


@app.get("/fetch/locations_general_details")
def fetch_locations_general_details(db: Session = Depends(get_db)):
    # This wouldn't work twice because a location is unique
    general_details_to_insert = []
    for location in LOCATIONS_TO_GEOCODE:
        coordinates = openweather.get_location_coordinates(location)
        details_in_schema = schemas.LocationGeneralDetails.parse_obj(
            {"lat": coordinates["lat"], "lon": coordinates["lon"], "location_name": location})
        general_details_to_insert.append(details_in_schema)
    return crud.create_locations_general_details(db, general_details_to_insert)


@app.get("/fetch/forecasts")
def fetch_forecasts(db: Session = Depends(get_db)):
    # This wouldn't work twice location_id and dt are a unique pair
    all_forecasts = []
    for location in crud.get_all_loactions_names(db):
        location_general_details = crud.get_location_general_details(
            db, location)
        hourly_forecast = openweather.get_hourly_weather_forecast(
            lat=location_general_details.lat, lon=location_general_details.lon)

        for one_hour_forecast in hourly_forecast:
            forecast_in_schema = schemas.Forecast.parse_obj(
                {**one_hour_forecast, "location_id": location_general_details.id})
            all_forecasts.append(forecast_in_schema)

    crud.create_forecasts(db, all_forecasts)


@app.get("/avg_tmp_per_city_per_day", response_model=List[schemas.AverageTempForCityPerDay])
def get_avg_tmp_per_city_per_day(db: Session = Depends(get_db)):
    avg_temp_per_city_per_day_list = []
    locations_names = crud.get_all_loactions_names(db)
    for location_name in locations_names:
        avg_temp_per_city_per_day_list.append({"location_name": location_name,
                                               "avg_temp_per_day": crud.get_average_temp_per_day(db, location_name)})
    return avg_temp_per_city_per_day_list


@app.get("/lowest_humid", response_model=schemas.Point)
def get_lowest_humidity_point(db: Session = Depends(get_db)):
    return crud.get_lowest_humidity_point(db)


@app.get("/feels_like_rank", response_model=List[schemas.LocationFeelsLike])
def get_feels_like_rank(order_dir: OrderDir = OrderDir.ascending, db: Session = Depends(get_db)):
    return crud.get_feels_like_rank(db, order_dir.value)
