"""
accuweather_client.py

This module provides an API client for interacting with the AccuWeather location API.
It includes classes for handling location-based requests, either by Point of Interest (POI)
or by city, and it validates the necessary inputs before making the requests.

Classes:
    - LocationBaseClient: Base class for handling location-based API requests.
    - LocationPOIClient: API client for fetching location data by Point of Interest (POI).
    - LocationCityClient: API client for fetching location data by city name.

Functions:
    - get_location_model: Factory function to initialize the correct client based on the input parameters.
"""

from typing import Any, Dict, Optional
from urllib import parse
from pydantic import model_validator
from requests import Session
from accuweather_client.models import TokenValidation, LocationModel


class LocationBaseClient(TokenValidation):
    """
    Base API client for interacting with the location API of AccuWeather.

    Attributes:
        session (Session): A requests session used for making HTTP requests.
        location (Optional[LocationModel]): The location model generated from the API response.
        query_url (Optional[str]): The URL used for making the location API request.
    """

    session: type = Session
    location: Optional[LocationModel] = None
    query_url: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def poi_or_city_validation(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates that the client is initiated with either a city or a POI.

        Args:
            values (Dict[str, Any]): The dictionary of values passed during initialization.

        Returns:
            Dict[str, Any]: The validated dictionary of values.

        Raises:
            ValueError: If neither 'city' nor 'poi' is provided in the values.
        """
        if not values.get("city") and not values.get("poi"):
            raise ValueError('At least one of "city" or "poi" must be provided.')
        return values

    @model_validator(mode="after")
    @classmethod
    def create_location_attribute(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates the location attribute by making a request to the AccuWeather API.

        Args:
            values (Dict[str, Any]): The dictionary of values passed during initialization.

        Returns:
            Dict[str, Any]: The dictionary of values with the location attribute added.

        Raises:
            ValueError: If the API request fails or if the location data could not be fetched.
        """
        loc_session = cls.model_fields["session"].default()
        try:
            response = loc_session.request(
                method="GET",
                url=values.query_url,
                params={"apikey": values.token, "details": "true"},
            )
            response.raise_for_status()
            values.location = LocationModel(response=response.json())
        except Exception as e:
            raise ValueError(f"Failed to fetch location data: {e}")
        return values


class LocationPOIClient(LocationBaseClient):
    """
    API client for fetching location data by Point of Interest (POI) from the AccuWeather API.

    Attributes:
        poi (str): The Point of Interest for which to fetch location data.
        base_url (str): The base URL for the POI search endpoint.
    """

    poi: str
    base_url: str = "http://dataservice.accuweather.com/locations/v1/poi/search?q="

    @model_validator(mode="before")
    @classmethod
    def set_location_attributes(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sets the query URL for the POI search based on the provided POI.

        Args:
            values (Dict[str, Any]): The dictionary of values passed during initialization.

        Returns:
            Dict[str, Any]: The dictionary of values with the query URL set.
        """
        url = f"{cls.model_fields['base_url'].default}{parse.quote(values.get('poi'))}"
        values["query_url"] = url
        return values


class LocationCityClient(LocationBaseClient):
    """
    API client for fetching location data by city name from the AccuWeather API.

    Attributes:
        city (str): The city name for which to fetch location data.
        country (Optional[str]): The country name associated with the city (optional).
        base_url (str): The base URL for the city search endpoint.
    """

    city: str
    country: Optional[str] = None
    base_url: str = "http://dataservice.accuweather.com/locations/v1/"

    @model_validator(mode="before")
    @classmethod
    def set_location_attributes(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sets the query URL for the city search based on the provided city and country.

        Args:
            values (Dict[str, Any]): The dictionary of values passed during initialization.

        Returns:
            Dict[str, Any]: The dictionary of values with the query URL set.
        """
        if not values.get("country"):
            url = f"{cls.model_fields['base_url'].default}cities/search?q={values['city']}"
        else:
            url = (
                f"{cls.model_fields['base_url'].default}search?q="
                f"{values['city']}%20{values['country']}"
            )
        values["query_url"] = url
        return values


def get_location_model(
    city: str = None, poi: str = None, **kwargs
) -> LocationBaseClient:
    """
    Factory function to initialize the correct location client based on the provided parameters.

    Args:
        city (str, optional): The city name for which to fetch location data.
        poi (str, optional): The Point of Interest for which to fetch location data.
        **kwargs: Additional keyword arguments passed to the client classes.

    Returns:
        LocationBaseClient: An instance of either LocationCityClient or LocationPOIClient.

    Raises:
        ValueError: If both 'city' and 'poi' are provided, or if neither is provided.
    """
    if city and poi:
        raise ValueError('Only one of "city" or "poi" can be provided, not both.')
    if city:
        return LocationCityClient(city=city, **kwargs)
    if poi:
        return LocationPOIClient(poi=poi, **kwargs)
    raise ValueError('You must provide either a "city" or a "poi".')
