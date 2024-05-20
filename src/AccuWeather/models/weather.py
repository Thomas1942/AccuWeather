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
