import requests
from AccuWeather.models import TokenValidation


class WeatherClient(TokenValidation, requests.Session):
    token: str
