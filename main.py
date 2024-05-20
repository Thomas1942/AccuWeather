"""This is the main scripts to test the code"""

from AccuWeather.clients import LocationClient, WeatherClient
from constant import API_KEY

loc_client = LocationClient(token=API_KEY)
result = loc_client.get_location(loc="amsterdam")
loc_key = result.get_location_key()
weather = WeatherClient(token=API_KEY, location_key=loc_key)
response = weather.get_5day_forecast()
response
