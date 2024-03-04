from __future__ import annotations

from typing import List

from pydantic import BaseModel, model_validator, validator

from frost.utils.validation import validate_time_range, validate_wkt


class IdfRequest(BaseModel):
    sources: str
    location: str
    durations: str
    frequencies: str
    unit: str

    @validator("sources")
    def sources_must_be_valid(cls, v):
        if v == "grid":
            return v

        station_ids = v.split(",")
        station_ids = [station_id.strip() for station_id in station_ids]

        # Check if the input is a list of integers
        if not all(station_id.isdigit() for station_id in station_ids):
            raise ValueError(
                """sources must be 'grid' or a comma-separated
                list of staion IDs (integers)"""
            )

        return v

    @validator("location")
    def location_must_be_valid(cls, v):
        if validate_wkt(v):
            return v
        else:
            raise ValueError(
                "Location must be format POINT(<longitude degrees> <latitude degrees>)."
            )

    @validator("durations")
    def validate_durations(cls, v):
        # Check if the input is a single or list of integers
        if v == "" | v == None:
            return v
        durations = v.split(",")
        if not all(duration.isdigit() for duration in durations):
            raise ValueError("Durations must be a comma-separated list of integers")

        return v

    @validator("frequencies")
    def validate_frequencies(cls, v):
        if v == "" | v == None:
            return v
        # Check if the input is a single or list of integers
        frequencies = v.split(",")
        if not all(frequency.isdigit() for frequency in frequencies):
            raise ValueError("Frequencies must be a comma-separated list of integers")

        return v

    @validator("unit")
    def validate_unit(cls, v):
        if v == "" | v == None:
            return v
        if v == "mm" | v == "lsha":
            return v
        else:
            raise ValueError("Unit must be 'mm' or 'lsha'")


class SpatialExtent(BaseModel):
    bottom: int
    left: int
    right: int
    top: int


class Value(BaseModel):
    duration: int
    frequency: int
    intensity: int
    lowerinterval: int
    upperinterval: int


class Source(BaseModel):
    masl: int
    sourceID: str
    spatialExtent: SpatialExtent
    updatedAt: str
    values: List[Value]


class IdfResponse(BaseModel):
    sources: List[Source]
    unit: str
