from typing import Any

import pandas as pd
from pydantic import BaseModel, computed_field


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
        temp_unit = day_dict["Temperature"]["Maximum"]["Unit"]
        rain = day_dict["Day"]["RainProbability"]
        return f"{text}, max temp is {temp}{temp_unit} and {rain}% chance of rain."

    def to_pandas_df(self) -> pd.DataFrame:
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
