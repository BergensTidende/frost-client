from pydantic import BaseModel, validator, model_validator, Field
from typing import Optional, List
import re
import json


class ObsMetNoFilterParams(BaseModel):
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

        return True

    @validator("nearest")
    def validate_nearest(cls, v):
        try:
            nearest_data = json.loads(v)
            if not isinstance(nearest_data, dict):
                raise ValueError("Nearest must be a JSON object")

            # Validate the structure of 'nearest'
            required_keys = {"maxdist", "maxcount", "points"}
            if not required_keys.issubset(nearest_data):
                raise ValueError(
                    f"Missing keys in nearest; required keys are: {required_keys}"
                )

            # Validate 'points'
            if not all(
                isinstance(point, dict) and "lon" in point and "lat" in point
                for point in nearest_data["points"]
            ):
                raise ValueError(
                    "Each point in nearest must be a dictionary with 'lon' and 'lat' keys"
                )

        except json.JSONDecodeError:
            raise ValueError("Nearest must be valid JSON")

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


class Value(BaseModel):
    elevation: str = Field(..., alias="elevation(masl/hs)")
    latitude: str
    longitude: str


class Location(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    value: Value


class Element(BaseModel):
    description: str
    id: str
    name: str
    unit: str


class GeometryLevel(BaseModel):
    unit: str
    value: str


class QualityValue(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    value: str


class Timeseries(BaseModel):
    geometry: GeometryLevel
    quality: dict
    timeoffset: str
    timeresolution: str


class Station(BaseModel):
    location: List[Location]
    shortname: str


class Extra(BaseModel):
    element: Element
    station: Station
    timeseries: Timeseries


class Id(BaseModel):
    level: int
    parameterid: int
    sensor: int
    stationid: int


class Header(BaseModel):
    id: Id
    extra: Extra
    available: dict


class TSeries(BaseModel):
    header: Header
    observations: Optional[
        str
    ]  # Assuming observations can have a different structure or be null


class FrostApiResponse(BaseModel):
    tstype: str
    tseries: List[TSeries]
