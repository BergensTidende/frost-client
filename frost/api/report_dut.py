from pydantic import BaseModel, model_validator, Field

from typing import List
from .reports import ReportResponse


class SourceId(BaseModel):
    type: str


class ReportDutRequest(BaseModel):
    source_id: SourceId = Field(..., alias="SourceID")

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if values.get("SourceID") == None:
            raise ValueError("SourceID must be provided")
        return values


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


class DUT(BaseModel):
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


class ReportDutResponse(ReportResponse[DUT]):
    pass
