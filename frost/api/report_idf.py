from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, model_validator, validator, Field

from frost.utils.validation import validate_time, validate_time_range, validate_wkt

from .reports import ReportResponse


class ReportIdfRequest(BaseModel):
    StationID: str
    Unit: str

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if values.get("StationID") == None & values.get("Unit") == None:
            raise ValueError("Both StationID and Unit must be provided")
        return values

    @validator("Unit")
    def check_valid_unit(cls, values):
        if values not in ["mm", "mm/h", "mm/24h", "mm/48h", "mm/72h"]:
            raise ValueError(
                "Unit must be one of 'mm', 'mm/h', 'mm/24h', 'mm/48h', 'mm/72h'"
            )
        return values


class FirstYearOfPeriod(BaseModel):
    type: str


class LastYearOfPeriod(BaseModel):
    type: str


class NumberOfSeasons(BaseModel):
    type: str


class SeedParameter(BaseModel):
    type: str


class Sourceid(BaseModel):
    type: str


class OperatingItems(BaseModel):
    type: str


class OperatingPeriods(BaseModel):
    items: OperatingItems
    type: str


class QualityClass(BaseModel):
    type: str


class Unit(BaseModel):
    type: str


class UpdatedAt(BaseModel):
    type: str


class Frequency(BaseModel):
    type: str


class Intensity(BaseModel):
    type: str


class Duration(BaseModel):
    type: str


class Lowerinterval(BaseModel):
    type: str


class Returnperiod(BaseModel):
    type: str


class Upperinterval(BaseModel):
    type: str


class ItemsProperties(BaseModel):
    duration: Duration
    frequency: Frequency
    intensity: Intensity
    lowerinterval: Lowerinterval
    upperinterval: Upperinterval


class Items(BaseModel):
    properties: ItemsProperties
    type: str


class Values(BaseModel):
    items: Items
    type: str


class Properties(BaseModel):
    first_year_of_period: FirstYearOfPeriod = Field(..., alias="firstYearOfPeriod")
    last_year_of_period: LastYearOfPeriod = Field(..., alias="lastYearOfPeriod")
    number_of_seasons: NumberOfSeasons = Field(..., alias="numberOfSeasons")
    operating_periods: OperatingPeriods = Field(..., alias="operatingPeriods")
    quality_class: QualityClass = Field(..., alias="qualityClass")
    seed_parameter: SeedParameter = Field(..., alias="seedParameter")
    sourceid: Sourceid
    unit: Unit
    updated_at: UpdatedAt = Field(..., alias="updatedAt")
    values: Values


class Idf(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: Properties
    required: List[str]
    type: str


class ReportIdfResponse(ReportResponse[List[Idf]]):
    pass
