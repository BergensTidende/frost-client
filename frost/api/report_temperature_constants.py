from pydantic import BaseModel, field_validator, Field
from typing import List
from .reports import ReportResponse


class ReportTemperatureConstantsRequest(BaseModel):
    station_id: int = Field(None, alias="StationID")

    class Config:
        populate_by_name = True

    @field_validator("station_id")
    @classmethod
    def check_required_fields(cls, value, info):
        if value is None:
            raise ValueError(f"{info.field_name} must be provided")
        return value


class Values(BaseModel):
    field_1: float = Field(..., alias="1")
    field_2: float = Field(..., alias="2")
    field_3: float = Field(..., alias="3")
    field_4: float = Field(..., alias="4")
    field_5: float = Field(..., alias="5")
    field_6: float = Field(..., alias="6")
    field_7: float = Field(..., alias="7")
    field_8: float = Field(..., alias="8")
    field_9: float = Field(..., alias="9")
    field_10: float = Field(..., alias="10")
    field_11: float = Field(..., alias="11")
    field_12: float = Field(..., alias="12")


class ReportTemperatureConstantsResponse(BaseModel):
    from_time: str = Field(..., alias="FromTime")
    to_time: str = Field(..., alias="ToTime")
    values: Values = Field(..., alias="Values")
