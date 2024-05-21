from typing_extensions import Unpack
from pydantic import computed_field, PrivateAttr, HttpUrl
from requests import Session
from AccuWeather.models import TokenValidation, LocationModel
from typing import Optional


class LocationClient(TokenValidation):
    token: str
    city: str
    base_url: HttpUrl = (
        "http://dataservice.accuweather.com/locations/v1/cities/search?q="
    )
    _session: Session = PrivateAttr(default_factory=Session)

    @computed_field
    @property
    def auth_url(self) -> str:
        """Creates the auth_url property."""
        return f"&apikey={self.token}"

    @computed_field
    @property
    def location(self) -> LocationModel:
        """Creates the location property."""
        url = self.base_url + self.city + self.auth_url
        return LocationModel(
            response=self._session.request(method="GET", url=url).json()
        )
