from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


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
    elevation_masl_hs_: str = Field(..., alias='elevation(masl/hs)')
    latitude: str
    longitude: str


class LocationItem(BaseModel):
    from_: str = Field(..., alias='from')
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
    from_: str = Field(..., alias='from')
    to: str
    value: str


class PerformanceItem(BaseModel):
    from_: str = Field(..., alias='from')
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
    from_: str = Field(..., alias='from')


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


class Model(BaseModel):
    data: Optional[Data] = None
