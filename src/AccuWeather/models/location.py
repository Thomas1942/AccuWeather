from pydantic import BaseModel


class LocationModelCityResult(BaseModel):

    Version: int
    Key: int
    Type: str
    Rank: int
    LocalizedName: str
    EnglishName: str
    PrimaryPostalCode: str
    Region: dict
    Country: dict
    AdministrativeArea: dict
    TimeZone: dict
    GeoPosition: dict
    IsAlias: bool
    SupplementalAdminAreas: list
    DataSets: list


class LocationModel(BaseModel):
    response: list[LocationModelCityResult]

    def get_location_key(self):

        return self.response[0].Key
