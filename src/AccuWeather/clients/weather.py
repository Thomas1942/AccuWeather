from pydantic import (
    computed_field,
    PrivateAttr,
    NonNegativeInt,
    HttpUrl,
)
from AccuWeather.models import TokenValidation, ForecastModel5Days, LocationModel
from AccuWeather.clients import LocationClient
from requests import Session


class WeatherClient(TokenValidation):
    token: str
    city: str
    base_url: HttpUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
    _session: Session = PrivateAttr(default_factory=Session)

    @computed_field
    @property
    def location_client(self) -> LocationClient:
        return LocationClient(token=self.token, city=self.city)

    @computed_field
    @property
    def location(self) -> LocationModel:
        return self.loc_client.location.response[0]

    @computed_field
    @property
    def location_key(self) -> NonNegativeInt:
        return self.location.Key

    @computed_field
    @property
    def url(self) -> HttpUrl:
        """Creates the auth_url property."""
        return f"{self.base_url}{self.location_key}?apikey={self.token}&details=true&metric=true"

    def get_5day_forecast(self, *args, **kwargs):
        """Method to obtain the location key that can be used to specify a location in other API requests."""
        return ForecastModel5Days(
            output=self._session.request(method="GET", url=self.url).json()
        )
