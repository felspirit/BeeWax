# BeeWax
- In server/openweather.py change OPENWEATHER_API_KEY to your https://openweathermap.org api key
- From the Beewax folder (not server folder) run 'uvicorn server.main:app'

- Go to http://127.0.0.1:8000/fetch/locations_general_details (to fetch the general details for the locations to the db)
- Go to http://127.0.0.1:8000/fetch/forecasts (to fetch the forecasts for these locations)
-   These functions won't work twice because of unique constraints and will throw exceptions if you try...
  
- You can go to http://127.0.0.1:8000/docs or http://127.0.0.1:8000/fetch/redocs to test the api (and also do the steps above)


🐝
