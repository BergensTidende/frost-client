from pydantic import BaseModel, field_validator, Field

from typing import List

class ReportDutRequest(BaseModel):
    source_id: str = Field(..., alias="SourceID")

    class Config:
        populate_by_name = True

    @field_validator("source_id")
    def check_required_fields(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value


class SummerItem(BaseModel):
    duration: int
    intensity: float
    lowerinterval: float
    retperiod: int
    upperinterval: float


class WinterItem(BaseModel):
    duration: int
    intensity: float
    lowerinterval: float
    retperiod: int
    upperinterval: float


class ReportDutResponse(BaseModel):
    first_year_of_period: int = Field(..., alias="firstYearOfPeriod")
    last_year_of_period: int = Field(..., alias="lastYearOfPeriod")
    number_of_seasons: int = Field(..., alias="numberOfSeasons")
    reference_period: str = Field(..., alias="referencePeriod")
    seed_parameter: int = Field(..., alias="seedParameter")
    sourceid: str
    summer: List[SummerItem]
    unit: str
    updated_at: str = Field(..., alias="updatedAt")
    winter: List[WinterItem]
