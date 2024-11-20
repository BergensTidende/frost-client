from typing import List

from pydantic import BaseModel, field_validator, ValidationInfo


class IdfAvailableRequest(BaseModel):
    sources: str

    @field_validator("sources")
    @classmethod
    def sources_must_be_valid(cls, v: str, info: ValidationInfo):
        if v == "grid":
            return v

        station_ids = v.split(",")
        station_ids = [station_id.strip() for station_id in station_ids]

        # Check if the input is a list of integers
        if not all(station_id.isdigit() for station_id in station_ids):
            raise ValueError(
                """"sources must be 'grid' or a comma-separated
                list of station IDs (integers)"""
            )

        return v


class SpatialExtent(BaseModel):
    bottom: float
    left: float
    top: float
    right: float


class Source(BaseModel):
    sourceID: str
    updatedAt: str
    spatialExtent: SpatialExtent
    durations: List[int]
    frequencies: List[int]


class IdfAvailableResponse(BaseModel):
    sources: List[Source]
