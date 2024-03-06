from typing import List

from pydantic import BaseModel, field_validator, Field

from .reports import ReportResponse


class ReportIdfRequest(BaseModel):
    station_id: int = Field(..., alias="StationID")
    unit: str = Field(..., alias="Unit")

    class Config:
        populate_by_name = True

    @field_validator("station_id")
    def check_required_fields(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value

    @field_validator("unit")
    def check_valid_unit(cls, values):
        if values not in ["mm", "mm/h", "mm/24h", "mm/48h", "mm/72h"]:
            raise ValueError(
                "Unit must be one of 'mm', 'mm/h', 'mm/24h', 'mm/48h', 'mm/72h'"
            )
        return values


class Values(BaseModel):
    duration: int
    frequency: int
    intensity: float
    lowerinterval: float
    upperinterval: float


class ReportIdfResponse(BaseModel):
    first_year_of_period: int = Field(..., alias="firstYearOfPeriod")
    last_year_of_period: int = Field(..., alias="lastYearOfPeriod")
    number_of_seasons: int = Field(..., alias="numberOfSeasons")
    operating_periods: List[str] = Field(..., alias="operatingPeriods")
    quality_class: int = Field(..., alias="qualityClass")
    seed_parameter: int = Field(..., alias="seedParameter")
    sourceid: str
    unit: str
    updated_at: str = Field(..., alias="updatedAt")
    values: List[Values]
