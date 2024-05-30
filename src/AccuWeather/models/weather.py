from pydantic import BaseModel, computed_field
from typing import Any
import pandas as pd


class ForecastModel5Days(BaseModel):
    output: dict[str, Any]

    @computed_field
    @property
    def text(self) -> str:
        return self.output["Headline"]["Text"]

    @computed_field
    @property
    def forecast_tomorrow(self) -> str:
        day_dict = self.output["DailyForecasts"][1]
        text = day_dict["Day"]["IconPhrase"].replace("w/", "with")
        temp = day_dict["Temperature"]["Maximum"]["Value"]
        rain = day_dict["Day"]["RainProbability"]
        return f"{text}, max temp is {temp}C and {rain}% chance of rain."

    def to_pandas_dict(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(self.output["DailyForecasts"])


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


class HistoricalConditionslModel(BaseModel):
    output: Any

    @computed_field
    @property
    def temperature(self) -> list[float]:
        temp = []
        for h in self.output:
            temp.append(
                h["TemperatureSummary"]["Past24HourRange"]["Maximum"]["Metric"]["Value"]
            )
        return temp
