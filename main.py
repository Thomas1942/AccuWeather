"""This is the main scripts to test the code"""

from AccuWeather.clients import WeatherClient
from constants import API_KEY

weather = WeatherClient(token=API_KEY, city="amsterdam")
response = weather.get_5day_forecast()
response
