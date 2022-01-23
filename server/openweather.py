import json
from urllib.parse import urlencode

import requests

OPENWEATHER_API_KEY = ""
OPENWEATHER_HOURLY_FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"
OPENWEATHER_GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"


def get_location_coordinates(location_name):
    query_string = urlencode(
        {"q": location_name, "appid": OPENWEATHER_API_KEY})
    complete_url = OPENWEATHER_GEOCODING_BASE_URL + "?" + query_string
    geocoding_json = requests.get(complete_url).content
    geocoding_dict = json.loads(geocoding_json)
    coordinate_lat = geocoding_dict[0]['lat']
    coordinate_lon = geocoding_dict[0]['lon']
    return {'lat': coordinate_lat, 'lon': coordinate_lon}


def get_hourly_weather_forecast(lat, lon):
    query_string = urlencode({"lat": lat, "lon": lon, "exclude": "current,minutely,daily",
                              "units": "metric", "appid": OPENWEATHER_API_KEY})
    complete_url = OPENWEATHER_HOURLY_FORECAST_BASE_URL + "?" + query_string

    full_forecast_json = requests.get(complete_url).content
    hourly_full_forecast = json.loads(full_forecast_json)['hourly']

    hourly_weather = []
    for one_hour_full_forecast in hourly_full_forecast:
        dt = one_hour_full_forecast["dt"]
        temp = one_hour_full_forecast["temp"]
        humidity = one_hour_full_forecast["humidity"]
        feels_like = one_hour_full_forecast["feels_like"]
        hourly_weather.append({
            "dt": dt,
            "temp": temp,
            "humidity": humidity,
            "feels_like": feels_like})

    return hourly_weather
