from typing_extensions import Unpack
from pydantic import computed_field, PrivateAttr, HttpUrl
from requests import Session
from AccuWeather.models import TokenValidation, LocationModel
from typing import Optional


class LocationClient(TokenValidation):
    token: str
    base_url: HttpUrl = (
        "http://dataservice.accuweather.com/locations/v1/cities/search?q="
    )
    _session: Session = PrivateAttr(default_factory=Session)

    @computed_field
    @property
    def auth_url(self) -> str:
        """Creates the auth_url property."""
        return f"&apikey={self.token}"

    def get_location(self, loc: str, *args, **kwargs) -> LocationModel:
        """Method to obtain the location key that can be used to specify a location in other API requests."""
        url = self.base_url + loc + self.auth_url
        return LocationModel(
            response=self._session.request(method="GET", url=url).json()
        )
