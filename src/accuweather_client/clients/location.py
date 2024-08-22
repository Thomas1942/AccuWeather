from typing import Any, Optional

from pydantic import model_validator
from requests import Session

from AccuWeather.models import LocationModel, TokenValidation


class LocationClient(TokenValidation):
    """API client for the location API of the accuweather API."""

    token: str
    city: str | None = None
    country: Optional[str] | None = None
    base_url: str = "http://dataservice.accuweather.com/locations/v1/"
    session: type = Session
    location: LocationModel | None = None

    @model_validator(mode="before")
    def create_location_attribute(cls, values: Any) -> Any:
        if values.get("country") is None:
            url = (
                cls.model_fields.get("base_url").default
                + "cities/search?q="
                + values.get("city")
            )
        else:
            url = (
                cls.model_fields.get("base_url").default
                + "search?q="
                + values.get("city")
                + "%20"
                + values.get("country")
            )
        loc_session = cls.model_fields.get("session").default()
        values["location"] = LocationModel(
            response=loc_session.request(
                method="GET",
                url=url,
                params={"apikey": values.get("token"), "details": "true"},
            ).json()
        )
        return values
