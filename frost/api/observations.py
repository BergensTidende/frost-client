import json
import re
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, validator

from frost.utils.validation import validate_nearest


class ObservationsRequest(BaseModel):
    incobs: bool = False
    time: str = "latest"
    elementids: str | None = None
    location: str | None = None
    stationids: str | None = None
    nearest: str | None = None
    polygon: str | None = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        fields = ["elementids", "location", "stationids", "nearest", "polygon"]
        if not any(values.get(field) is not None for field in fields):
            raise ValueError(
                "At least one of elementids, location, stationids, nearest, polygon must be provided"
            )
        return values

    @validator("time")
    def time_must_be_valid(cls, v):
        # Regular expression for the time range format
        time_range_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"

        # Check if the input is either 'latest' or matches the time range pattern
        if v != "latest" and not re.match(time_range_pattern, v):
            raise ValueError(
                "time must be 'latest' or in the format 'YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ'"
            )
        return v

    @validator("nearest")
    def validate_nearest(cls, v):
        if validate_nearest(v):
            return v

    @validator("polygon")
    def validate_polygon(cls, v):
        try:
            polygon_data = json.loads(v)
            if not isinstance(polygon_data, list):
                raise ValueError("Polygon must be a JSON array")

            # Validate each point in the polygon
            if not all(
                isinstance(point, dict) and "lon" in point and "lat" in point
                for point in polygon_data
            ):
                raise ValueError(
                    "Each point in polygon must be a dictionary with 'lon' and 'lat' keys"
                )

        except json.JSONDecodeError:
            raise ValueError("Polygon must be valid JSON")

        return v


class Id(BaseModel):
    level: int
    parameterid: int
    sensor: int
    stationid: int


class Element(BaseModel):
    description: str
    id: str
    name: str
    unit: str


class Value(BaseModel):
    elevation_masl_hs_: str = Field(..., alias="elevation(masl/hs)")
    latitude: str
    longitude: str


class LocationItem(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    value: Value


class Station(BaseModel):
    location: List[LocationItem]
    shortname: str


class Level(BaseModel):
    unit: str
    value: str


class Geometry(BaseModel):
    level: Level


class ExposureItem(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    value: str


class PerformanceItem(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    value: str


class Quality(BaseModel):
    exposure: List[ExposureItem]
    performance: List[PerformanceItem]


class Timeseries(BaseModel):
    geometry: Geometry
    quality: Quality
    timeoffset: str
    timeresolution: str


class Extra(BaseModel):
    element: Element
    station: Station
    timeseries: Timeseries


class Available(BaseModel):
    from_: str = Field(..., alias="from")


class Header(BaseModel):
    id: Id
    extra: Extra
    available: Available


class Body(BaseModel):
    qualitycode: str
    value: str


class Observation(BaseModel):
    time: str
    body: Body


class Tsery(BaseModel):
    header: Header
    observations: List[Observation]


class Data(BaseModel):
    tstype: str
    tseries: List[Tsery]


class ObservationsResponse(BaseModel):
    data: Data