"""
weather_client.py

This module provides an API client for interacting with the AccuWeather API
to retrieve weather data, including current conditions and a 5-day forecast.

Example:
    client = WeatherClient(token="your_api_key", city="New York")
    forecast = client.get_5day_forecast()
    print(forecast)

Classes:
    - WeatherClient: API client for fetching current conditions and 5-day forecasts.
"""

from typing import Any, Dict, Optional

from pydantic import PrivateAttr, model_validator
from requests import Session
from requests.exceptions import RequestException

from accuweather_client.clients import LocationBaseClient, get_location_model
from accuweather_client.models import (
    CurrentConditionsModel,
    ForecastModel5Days,
    LocationModelItem,
    TokenValidation,
)


class WeatherClient(TokenValidation):
    """
    AccuWeather API client for retrieving a 5-day weather forecast and current weather conditions.

    Attributes:
        token (str): API token for authenticating requests to the AccuWeather API.
        city (Optional[str]): The city name for which to fetch weather data.
        country (Optional[str]): The country associated with the city (optional).
        poi (Optional[str]): The Point of Interest for which to fetch weather data.
        base_url (str): The base URL for the AccuWeather API endpoints.
        _session (Session): A requests session used for making HTTP requests.
        location_client (Optional[LocationBaseClient]): Client for fetching location-related data.
        location (Optional[LocationModel]): Location data model retrieved from the location client.
        location_key (Optional[str]): The location key used to specify a location in API requests.
    """

    city: Optional[str] = None
    country: Optional[str] = None
    poi: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    base_url: str = "http://dataservice.accuweather.com/"
    _session: Session = PrivateAttr(default_factory=Session)
    location_client: Optional[LocationBaseClient] = None
    location: Optional[LocationModelItem] = None
    location_key: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def create_location_attributes(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Initializes location-related attributes when an instance of WeatherClient is created.

        This method sets up the `location_client`, `location`, and `location_key` attributes
        based on the provided city, country, or POI.

        Args:
            values (Dict[str, Any]): The dictionary of values passed during initialization.

        Returns:
            Dict[str, Any]: The dictionary of values with the location-related attributes added.
        """
        location_client = get_location_model(
            token=values.get("token"),
            city=values.get("city"),
            country=values.get("country"),
            poi=values.get("poi"),
            lat=values.get("lat"),
            lon=values.get("lon"),
        )
        location = (
            location_client.location.response[0]
            if isinstance(location_client.location.response, list)
            else location_client.location.response
        )
        location_key = location.Key

        # Directly update the values dictionary
        values.update(
            {
                "location_client": location_client,
                "location": location,
                "location_key": location_key,
            }
        )
        return values

    def _make_request(self, endpoint: str) -> dict:
        """
        Helper method to make API requests to the AccuWeather API.

        Args:
            endpoint (str): The API endpoint to query.

        Returns:
            dict: The JSON response from the API.

        Raises:
            RequestException: If the API request fails.
        """
        url = self.base_url + endpoint + str(self.location_key)
        try:
            response = self._session.request(
                method="GET",
                url=url,
                params={"apikey": self.token, "details": "true"},
            )
            response.raise_for_status()  # Raise error for bad responses
            return response.json()
        except RequestException as e:
            raise RequestException(
                f"Failed to retrieve data from {url}"
            ) from e

    def get_5day_forecast(self) -> ForecastModel5Days:
        """
        Retrieves the 5-day weather forecast for the specified location.

        Returns:
            ForecastModel5Days: A model containing the 5-day weather forecast data.
        """
        return ForecastModel5Days(
            output=self._make_request("forecasts/v1/daily/5day/")
        )

    def get_current_conditions(self) -> CurrentConditionsModel:
        """
        Retrieves the current weather conditions for the specified location.

        Returns:
            CurrentConditionsModel: A model containing the current weather conditions data.
        """
        return CurrentConditionsModel(
            output=self._make_request("currentconditions/v1/")
        )
