from typing import Any, Dict, Optional
from pydantic import model_validator
from requests import Session

from accuweather_client.models import LocationModel, TokenValidation


class LocationClient(TokenValidation):
    """API client for the location API of the accuweather API."""

    token: str
    city: str | None = None
    country: Optional[str] | None = None
    base_url: str = "http://dataservice.accuweather.com/locations/v1/"
    query_url: str | None = None
    session: type = Session
    location: LocationModel | None = None

    @model_validator(mode="before")
    def set_location_attributes(cls, values: dict) -> dict:
        if not values.get("country"):
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
        values["query_url"] = url
        return values

    @model_validator(mode="after")
    def create_location_attribute(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        loc_session = cls.model_fields.get("session").default()
        values.location = LocationModel(
            response=loc_session.request(
                method="GET",
                url=values.query_url,
                params={"apikey": values.token, "details": "true"},
            ).json()
        )
        return values
