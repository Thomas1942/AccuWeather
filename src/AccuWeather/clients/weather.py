from pydantic import (
    computed_field,
    PrivateAttr,
    NonNegativeInt,
    HttpUrl,
)
from AccuWeather.models import (
    TokenValidation,
    ForecastModel5Days,
    LocationModel,
    CurrentConditionsModel,
)
from AccuWeather.clients import LocationClient
from requests import Session


class WeatherClient(TokenValidation):
    token: str
    city: str
    base_url: HttpUrl = "http://dataservice.accuweather.com/"
    _session: Session = PrivateAttr(default_factory=Session)

    @computed_field
    @property
    def location_client(self) -> LocationClient:
        return LocationClient(token=self.token, city=self.city)

    @computed_field
    @property
    def location(self) -> LocationModel:
        return self.location_client.location.response[0]

    @computed_field
    @property
    def location_key(self) -> NonNegativeInt:
        return self.location.Key

    def get_5day_forecast(self, *args, **kwargs) -> ForecastModel5Days:
        """Method to obtain the location key that can be used to specify a location in other API requests."""
        url = self.base_url + "forecasts/v1/daily/5day/" + str(self.location_key)
        return ForecastModel5Days(
            output=self._session.request(
                method="GET", url=url, params={"apikey": self.token, "details": "true"}
            ).json()
        )

    def get_current_conditions(self, *args, **kwargs) -> CurrentConditionsModel:
        """Method to obtain the current weather conditions for a specific location."""
        url = self.base_url + "currentconditions/v1/" + str(self.location_key)
        return CurrentConditionsModel(
            output=self._session.request(
                method="GET", url=url, params={"apikey": self.token, "details": "true"}
            ).json()
        )
