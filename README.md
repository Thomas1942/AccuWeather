# AccuWeather
A python library to interact with the accuweather api.

## General information
For now, there is only basic functionality included in this package.
However, I hope to add more features in the future.

The functionality that makes this package unique is the integration of the
location client within the weather client. Specifying location by city name (and country optionally) is a more user-friendly way to interact with the api.

## Before you start
You need to create an api token on the AccuWeather website (https://developer.accuweather.com).

## How to use the package
```python
""""Some code to show the functionality of the package"""

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
