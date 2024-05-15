"""This is the main scripts to test the code"""

from AccuWeather.clients import LocationClient
from constant import API_KEY

loc_client = LocationClient(token=API_KEY)
result = loc_client.get_location(loc="amsterdam")
loc_key = result.get_location_key()
print(loc_key)
