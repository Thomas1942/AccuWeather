from pydantic import (
    computed_field,
    PrivateAttr,
    NonNegativeInt,
    HttpUrl,
)
from AccuWeather.models import TokenValidation, ForecastModel5Days
from AccuWeather.clients import LocationClient
from requests import Session


class WeatherClient(TokenValidation):
    token: str
    city: str
    base_url: HttpUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
    _session: Session = PrivateAttr(default_factory=Session)

    @computed_field
    @property
    def location_key(self) -> str:
        loc_client = LocationClient(token=self.token)
        result = loc_client.get_location(loc=self.city)
        return result.get_location_key()

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
        # return self._session.request(method="GET", url=self.url).json()
