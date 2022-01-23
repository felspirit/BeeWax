from typing import List

import sqlalchemy
from server import schemas
from sqlalchemy.orm import Session

from . import models


def create_locations_general_details(db: Session, locations_general_details: List[schemas.LocationGeneralDetails]):
    for details in locations_general_details:
        location_details_in_model = models.LocationGeneralDetails(
            location_name=details.location_name, lat=details.lat, lon=details.lon)
        db.add(location_details_in_model)
    db.commit()


def get_location_general_details(db: Session, location_name: str):
    return db.query(models.LocationGeneralDetails).filter(models.LocationGeneralDetails.location_name == location_name).first()


def get_all_loactions_names(db: Session):
    return [row.location_name for row in db.query(models.LocationGeneralDetails.location_name).all()]


def create_forecasts(db: Session, forecasts: List[schemas.Forecast]):
    for forecast in forecasts:
        forecast_in_model = models.Forecast(dt=forecast.dt, humidity=forecast.humidity,
                                            temp=forecast.temp, feels_like=forecast.feels_like, location_id=forecast.location_id)
        db.add(forecast_in_model)
    db.commit()


def get_average_temp_per_day(db: Session, location_name: str):
    return db.query(models.Forecast.dt,
                    sqlalchemy.func.avg(models.Forecast.temp).label("avg_temp")).filter(
        models.Forecast.location.has(location_name=location_name)).group_by(
            sqlalchemy.func.strftime("%d", models.Forecast.dt)).all()


def get_lowest_humidity_point(db: Session):
    return db.query(models.Forecast.dt,
                    models.LocationGeneralDetails.location_name,
                    sqlalchemy.func.min(models.Forecast.humidity).label("min_humidity")).join(
        models.LocationGeneralDetails).first()


def get_feels_like_rank(db: Session, order_dir="asc"):
    if order_dir not in ["asc", "desc"]:
        raise ValueError("'Order' parameter should be 'asc' or 'desc'")

    unordered_query = db.query(models.LocationGeneralDetails.location_name,
                               models.Forecast.feels_like,
                               sqlalchemy.func.max(models.Forecast.dt)).join(
        models.LocationGeneralDetails).group_by(
        models.Forecast.location_id)

    if order_dir == "asc":
        return unordered_query.order_by(sqlalchemy.asc(models.Forecast.feels_like)).all()
    elif order_dir == "desc":
        return unordered_query.order_by(sqlalchemy.desc(models.Forecast.feels_like)).all()
