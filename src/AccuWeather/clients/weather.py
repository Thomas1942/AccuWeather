from typing import Any, Optional

from pydantic import (
    NonNegativeInt,
    PrivateAttr,
    model_validator,
)
from requests import Session

from AccuWeather.clients import LocationClient
from AccuWeather.models import (
    CurrentConditionsModel,
    ForecastModel5Days,
    LocationModelCity,
    TokenValidation,
)


class WeatherClient(TokenValidation):
    """Accuweather API client to get a 5 day forecast and the current
    conditions."""

    token: str
    city: str
    country: Optional[str] | None = None
    base_url: str = "http://dataservice.accuweather.com/"
    _session: Session = PrivateAttr(default_factory=Session)
    location_client: LocationClient | None = None
    location: LocationModelCity | None = None
    location_key: NonNegativeInt | None = None

    @model_validator(mode="before")
    def compute_location_attributes(cls, values: Any) -> Any:
        """Creates the fixed attributes that created from other attributes
        when an instance is created."""
        values["location_client"] = LocationClient(
            token=values.get("token"),
            city=values.get("city"),
            country=values.get("country"),
        )
        values["location"] = values["location_client"].location.response[0]
        values["location_key"] = values["location"].Key
        return values

    def get_5day_forecast(self) -> ForecastModel5Days:
        """Method to obtain the location key that can be used to specify a
        location in other API requests."""
        url = self.base_url + "forecasts/v1/daily/5day/" + str(self.location_key)
        return ForecastModel5Days(
            output=self._session.request(
                method="GET", url=url, params={"apikey": self.token, "details": "true"}
            ).json()
        )

    def get_current_conditions(self) -> CurrentConditionsModel:
        """Method to obtain the current weather conditions for a specific location."""
        url = self.base_url + "currentconditions/v1/" + str(self.location_key)
        return CurrentConditionsModel(
            output=self._session.request(
                method="GET", url=url, params={"apikey": self.token, "details": "true"}
            ).json()
        )
