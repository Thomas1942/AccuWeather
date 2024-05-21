"""This is the main scripts to test the code"""

from AccuWeather.clients import WeatherClient
from constants import API_KEY

weather = WeatherClient(token=API_KEY, city="amsterdam")
forecast = weather.get_5day_forecast()
forecast.forecast_tomorrow
forecast.to_pandas_dict()

# Current conditions
# Forecast daily
# Forecast hourly
