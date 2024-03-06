from typing import List, Optional

from pydantic import BaseModel, field_validator, Field

from frost.utils.validation import validate_time

from .reports import ScaleType, ReportResponse


class ReportWindroseRequest(BaseModel):
    station_id: int = Field(..., alias="StationID")
    from_time: str = Field(..., alias="FromTime")
    to_time: str = Field(..., alias="ToTime")
    months: Optional[List[int]] = Field(None, alias="Months")
    max_wind_speed: Optional[int] = Field(None, alias="MaxWindSpeed")
    scale: Optional[ScaleType] = Field(None, alias="Scale")

    class Config:
        populate_by_name = True

    @field_validator("station_id", "from_time", "to_time")
    @classmethod
    def check_required_fields(cls, value):
        if value is None:
            raise ValueError(
                "All of station_id, from_time and to_time must be provided"
            )
        return value

    @field_validator("from_time", "to_time")
    @classmethod
    def check_valid_from_time(cls, value, info):
        return validate_time(value, info.field_name)


class Extras(BaseModel):
    title: str
    value: float

class Metadata(BaseModel):
    automatic_data: Optional[List[str]] = Field(..., alias="automaticData")
    from_time: str = Field(..., alias="fromTime")
    manual_data: Optional[List[str]] = Field(..., alias="manualData")
    months: Optional[List[str]]
    number_of_values: int = Field(..., alias="numberOfValues")
    station_id: str = Field(..., alias="stationID")
    to_time: str = Field(..., alias="toTime")


class Axis(BaseModel):
    name: str
    sums: List[float]
    titles: List[str]


class ReportWindroseResponse(BaseModel):
    extras: List[Extras]
    horizontal_axis: Axis = Field(..., alias="horizontalAxis")
    metadata: Metadata
    table: List[List[float]]
    vertical_axis: Axis = Field(..., alias="verticalAxis")
