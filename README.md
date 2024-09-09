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
import pandas as pd

# Create an instance of the WeatherClient class, a regular search
weather = WeatherClient(token=API_KEY, city="sydney")
# # Provides information about the location
weather.location

# In the example above, the selected location is Sydney, Australia
# If you like to select Sydney in Canada, you can refine your search with
# the addition of the country parameter
weather = WeatherClient(token=API_KEY, city="sydney", country="canada")
weather.location

# Create an instance of the WeatherClient class, POI search
weather = WeatherClient(token=API_KEY, poi="Eiffel tower")
weather.location

# Create an instance of the WeatherClient class, lat lon search
weather = WeatherClient(token=API_KEY, lat=51.988, lon=-4.88)
weather.location

# Creates an object that yields forecast information
forecast = weather.get_5day_forecast()
# Prints the forecast for tomorrow
forecast.forecast_tomorrow
# Returns a pandas df with forecast information
forecast_df = forecast.to_pandas_df()
# Parse the day column and add to df
forecast_df_parsed = pd.concat(
    [forecast_df, pd.json_normalize(forecast_df["Day"])], axis=1
)

# Creates an object that yiels information about the current conditions
conditions = weather.get_current_conditions()
# Prints the current conditions
conditions.current_conditions
