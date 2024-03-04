from pydantic import BaseModel, model_validator, Field
from typing import List
from .reports import ReportResponse


class ReportNormalsRequest(BaseModel):
    ElementID: str
    Period: str
    StationID: int

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if (
            values.get("ElementID")
            == None & values.get("Period")
            == None & values.get("StationID")
            == None
        ):
            raise ValueError("Both ElementID, Period and StationID must be provided")
        return values


class Day(BaseModel):
    type: str


class Month(BaseModel):
    type: str


class Normal(BaseModel):
    type: str


class ItemsProperties(BaseModel):
    day: Day = Field(..., alias="Day")
    month: Month = Field(..., alias="Month")
    normal: Normal = Field(..., alias="Normal")


class Items(BaseModel):
    properties: ItemsProperties
    required: List[str]
    type: str


class Normals(BaseModel):
    items: Items
    type: str


class Properties(BaseModel):
    normals: Normals = Field(..., alias="Normals")


class NormalsResponse(BaseModel):
    properties: Properties
    required: List[str]
    type: str


class ReportNormalsResponse(ReportResponse[NormalsResponse]):
    pass
