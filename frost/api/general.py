import json
import re
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, validator


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
    observations: Optional[str]


class FrostApiResponse(BaseModel):
    tstype: str
    tseries: List[TSeries]
