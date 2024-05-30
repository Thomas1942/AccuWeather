"""This is the main scripts to test the code"""

from AccuWeather.clients import WeatherClient
from constants import API_KEY

weather = WeatherClient(token=API_KEY, city="sydney", country="canada")
weather.location
# forecast = weather.get_5day_forecast()
# forecast.forecast_tomorrow
# forecast.to_pandas_dict()

conditions = weather.get_current_conditions()
conditions.current_conditions
hist_conditions = weather.get_historical_conditions()

hist_conditions.temperature
