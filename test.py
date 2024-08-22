"""This is the main scripts to test the code"""

from accuweather_client.clients import WeatherClient
from constants import API_KEY

# Create an instance of the WeatherClient class
weather = WeatherClient(token=API_KEY, city="sydney", country="canada")
# Provides information about the location
weather.location

# The country argument for the WeatherClient instance is optional
# The code below would give you the location for Syndey, Australia
weather = WeatherClient(token=API_KEY, city="sydney")

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
