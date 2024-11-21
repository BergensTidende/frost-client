import json
import re
from typing import List

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from frost.utils.validation import validate_nearest


class ObservationsRequest(BaseModel):
    include_observations: bool = Field(True, alias="incobs")
    time: str = "latest"
    element_ids: str | None = Field(None, alias="elementids")
    location: str | None = None
    station_ids: str | None = Field(None, alias="stationids")
    nearest: str | None = None
    polygon: str | None = None

    class Config:
        populate_by_name = True

    @field_validator("include_observations", "time")
    @classmethod
    def check_required_fields(cls, value: str, field: ValidationInfo) -> str:
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value

    @field_validator("time")
    @classmethod
    def time_must_be_valid(cls, v: str) -> str:
        # Regular expression for the time range format
        time_range_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"  # noqa: E501 # pylint: disable=line-too-lon

        # Check if the input is either 'latest' or matches the time range pattern
        if v != "latest" and not re.match(time_range_pattern, v):
            raise ValueError(
                """time must be 'latest' or in the format
                'YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ'"""
            )
        return v

    @field_validator("nearest")
    @classmethod
    def validate_nearest(cls, v: str) -> str:
        if validate_nearest(v):
            return v
        else:
            raise ValueError("Invalid nearest value")

    @field_validator("polygon")
    @classmethod
    def validate_polygon(cls, v: str) -> str:
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
                    """Each point in polygon must be a dictionary with
                    'lon' and 'lat' keys"""
                )

        except json.JSONDecodeError as e:
            raise ValueError("Polygon must be valid JSON") from e

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
    elevation_masl_hs: str = Field(..., alias="elevation(masl/hs)")
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


class ObservationsResponse(BaseModel):
    tstype: str
    tseries: List[Tsery]
