from pydantic import BaseModel, field_validator, Field
from typing import List, Optional


class ReportNormalsRequest(BaseModel):
    element_id: str = Field(..., alias="ElementID")
    period: str = Field(..., alias="Period")
    station_id: int = Field(..., alias="StationID")

    class Config:
        populate_by_name = True

    @field_validator("element_id", "period", "station_id")
    def check_required_fields(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value


class Normals(BaseModel):
    day: Optional[int] = Field(..., alias="Day")
    month: Optional[int] = Field(..., alias="Month")
    normal: int = Field(..., alias="Normal")


class ReportNormalsResponse(BaseModel):
    normals: List[Normals] = Field(..., alias="Normals")
