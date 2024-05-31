"""This is the main scripts to test the code"""

from AccuWeather.clients import WeatherClient
from constants import API_KEY

# Create an instance of the WeatherClient class
weather = WeatherClient(token=API_KEY, city="sydney", country="canada")
# Provides information about the location
weather.location

# Creates an instance that yields forecast information
forecast = weather.get_5day_forecast()
# Prints the forecast for tomorrow
forecast.forecast_tomorrow
# Returns a pandas df with forecast information
forecast.to_pandas_df()

# Creates an instance that yiels information about the current conditions
conditions = weather.get_current_conditions()
# Prints the current conditions
conditions.current_conditions

# Work in progress
hist_conditions = weather.get_historical_conditions()
hist_conditions.temperature
