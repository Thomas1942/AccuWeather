from typing import Any, List, Optional

import pandas as pd
from pydantic import BaseModel, computed_field, Field


class TemperatureModel(BaseModel):
    value: float = Field(..., alias="Value")
    unit: str = Field(..., alias="Unit")
    unit_type: int = Field(..., alias="UnitType")


class WindSpeedModel(BaseModel):
    value: float = Field(..., alias="Value")
    unit: str = Field(..., alias="Unit")
    unit_type: int = Field(..., alias="UnitType")


class WindDirectionModel(BaseModel):
    degrees: int = Field(..., alias="Degrees")
    localized: str = Field(..., alias="Localized")
    english: str = Field(..., alias="English")


class WindModel(BaseModel):
    speed: WindSpeedModel = Field(..., alias="Speed")
    direction: WindDirectionModel = Field(..., alias="Direction")


class WindGustModel(BaseModel):
    speed: WindSpeedModel = Field(..., alias="Speed")


class DayNightForecastModel(BaseModel):
    icon: int = Field(..., alias="Icon")
    icon_phrase: str = Field(..., alias="IconPhrase")
    has_precipitation: bool = Field(..., alias="HasPrecipitation")
    wind: WindModel = Field(..., alias="Wind")
    wind_gust: WindGustModel = Field(..., alias="WindGust")
    precipitation_probability: int = Field(
        ..., alias="PrecipitationProbability"
    )


class DailyForecastModel(BaseModel):
    date: str = Field(..., alias="Date")
    epoch_date: int = Field(..., alias="EpochDate")
    temperature: dict = Field(..., alias="Temperature")
    day: DayNightForecastModel = Field(..., alias="Day")
    night: DayNightForecastModel = Field(..., alias="Night")
    sources: List[str] = Field(..., alias="Sources")
    mobile_link: str = Field(..., alias="MobileLink")
    link: str = Field(..., alias="Link")


class HeadlineModel(BaseModel):
    effective_date: str = Field(..., alias="EffectiveDate")
    effective_epoch_date: int = Field(..., alias="EffectiveEpochDate")
    severity: int = Field(..., alias="Severity")
    text: str = Field(..., alias="Text")
    category: str = Field(..., alias="Category")
    end_date: str = Field(..., alias="EndDate")
    end_epoch_date: int = Field(..., alias="EndEpochDate")
    mobile_link: str = Field(..., alias="MobileLink")
    link: str = Field(..., alias="Link")


class ForecastModel(BaseModel):
    date_time: str = Field(..., alias="DateTime")

    epoch_date_time: int = Field(..., alias="EpochDateTime")
    weather_icon: int = Field(..., alias="WeatherIcon")
    icon_phrase: str = Field(..., alias="IconPhrase")
    has_precipitation: bool = Field(..., alias="HasPrecipitation")
    precipitation_type: Optional[str] = Field(None, alias="PrecipitationType")
    precipitation_intensity: Optional[str] = Field(
        None, alias="PrecipitationIntensity"
    )

    is_daylight: bool = Field(..., alias="IsDaylight")
    temperature: TemperatureModel = Field(..., alias="Temperature")
    real_feel_temperature: TemperatureModel = Field(
        ..., alias="RealFeelTemperature"
    )
    real_feel_temperature_shade: TemperatureModel = Field(
        ..., alias="RealFeelTemperatureShade"
    )

    wet_bulb_temperature: TemperatureModel = Field(
        ..., alias="WetBulbTemperature"
    )
    dew_point: TemperatureModel = Field(..., alias="DewPoint")
    wind: WindModel = Field(..., alias="Wind")
    wind_gust: WindGustModel = Field(..., alias="WindGust")

    relative_humidity: int = Field(..., alias="RelativeHumidity")
    indoor_relative_humidity: int = Field(..., alias="IndoorRelativeHumidity")
    visibility: TemperatureModel = Field(..., alias="Visibility")
    cloud_cover: int = Field(..., alias="CloudCover")
    ceiling: TemperatureModel = Field(..., alias="Ceiling")

    uv_index: int = Field(..., alias="UVIndex")
    uv_index_text: str = Field(..., alias="UVIndexText")
    precipitation_probability: int = Field(
        ..., alias="PrecipitationProbability"
    )
    thunderstorm_probability: int = Field(..., alias="ThunderstormProbability")
    rain_probability: int = Field(..., alias="RainProbability")
    snow_probability: int = Field(..., alias="SnowProbability")
    ice_probability: int = Field(..., alias="IceProbability")


class ForecastModel5Days(BaseModel):
    headline: HeadlineModel = Field(..., alias="Headline")
    daily_forecasts: List[DailyForecastModel] = Field(
        ..., alias="DailyForecasts"
    )

    @classmethod
    def from_api_response(cls, data: dict):
        return cls(**data)

    @computed_field
    @property
    def text(self) -> str:
        return self.headline.text

    @computed_field
    @property
    def forecast_tomorrow(self) -> str:
        day_dict = self.daily_forecasts[1]
        text = day_dict.day.icon_phrase.replace("w/", "with")
        temp = day_dict.temperature["Maximum"]["Value"]
        temp_unit = day_dict.temperature["Maximum"]["Unit"]
        rain = day_dict.day.precipitation_probability
        return f"{text}, max temp is {temp}{temp_unit} and {rain}% chance of rain."

    def to_pandas_df(self) -> pd.DataFrame:
        forecast_dicts = [
            forecast.dict(by_alias=True) for forecast in self.daily_forecasts
        ]
        return pd.json_normalize(forecast_dicts)


class HourlyForecastModel(BaseModel):
    output: List[ForecastModel]


class CurrentConditionsModel(BaseModel):
    output: list[dict[str, Any]]

    @computed_field
    @property
    def current_conditions(self) -> str:
        info = self.output[0]
        text = info["WeatherText"]
        temp = info["Temperature"]["Metric"]["Value"]
        temp_unit = info["Temperature"]["Metric"]["Unit"]
        wind_speed = info["Wind"]["Speed"]["Metric"]["Value"]
        wind_direction = info["Wind"]["Direction"]["Localized"]
        wind_unit = info["Wind"]["Speed"]["Metric"]["Unit"]
        return f"At the moment: {text.lower()}, with a temperature of {temp}{temp_unit}. The wind is comming from the {wind_direction} at {wind_speed}{wind_unit}."
