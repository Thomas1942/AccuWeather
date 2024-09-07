from pydantic import BaseModel
from typing import List, Optional


class Region(BaseModel):
    ID: str
    LocalizedName: str
    EnglishName: str


class Country(BaseModel):
    ID: str
    LocalizedName: str
    EnglishName: str


class AdministrativeArea(BaseModel):
    ID: str
    LocalizedName: str
    EnglishName: str
    Level: int
    LocalizedType: str
    EnglishType: str
    CountryID: str


class TimeZone(BaseModel):
    Code: str
    Name: str
    GmtOffset: float
    IsDaylightSaving: bool
    NextOffsetChange: Optional[str]


class Metric(BaseModel):
    Value: float
    Unit: str
    UnitType: int


class Imperial(BaseModel):
    Value: float
    Unit: str
    UnitType: int


class Elevation(BaseModel):
    Metric: Metric
    Imperial: Imperial


class GeoPosition(BaseModel):
    Latitude: float
    Longitude: float
    Elevation: Elevation


class SupplementalAdminArea(BaseModel):
    Level: int
    LocalizedName: str
    EnglishName: str


class Source(BaseModel):
    DataType: str
    Source: str
    SourceId: int
    PartnerSourceUrl: Optional[str] = None


class DMAModel(BaseModel):
    ID: str
    EnglishName: str
    Key: int


class Details(BaseModel):
    Key: str
    StationCode: str
    StationGmtOffset: float
    BandMap: str
    Climo: str
    LocalRadar: str
    MediaRegion: Optional[str]
    Metar: str
    NXMetro: str
    NXState: str
    Population: Optional[int]
    PrimaryWarningCountyCode: str
    PrimaryWarningZoneCode: str
    Satellite: str
    Synoptic: str
    MarineStation: str
    MarineStationGMTOffset: Optional[float]
    VideoCode: str
    LocationStem: str
    PartnerID: None
    Sources: List[Source]
    CanonicalPostalCode: str
    CanonicalLocationKey: str
    DMA: Optional[DMAModel] = None


class ParentCityModel(BaseModel):
    Key: str
    LocalizedName: str
    EnglishName: str


class LocationModelItem(BaseModel):
    Version: int
    Key: str
    Type: str
    Rank: int
    LocalizedName: str
    EnglishName: str
    PrimaryPostalCode: str
    Region: Region
    Country: Country
    AdministrativeArea: AdministrativeArea
    TimeZone: TimeZone
    GeoPosition: GeoPosition
    IsAlias: bool
    SupplementalAdminAreas: List[SupplementalAdminArea]
    DataSets: List[str]
    Details: Details
    ParentCity: Optional[ParentCityModel] = None


class LocationModel(BaseModel):
    response: list[LocationModelItem] | LocationModelItem

    def get_location_key(self):
        return self.response[0].Key
