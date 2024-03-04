from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, RootModel, validator

from frost.utils.validation import validate_time_range, validate_wkt

from .reports import FormatType


class LightningRequest(BaseModel):
    referencetime: str
    format: FormatType
    geometry: Optional[str] = None

    @validator("referencetime", "format", pre=True, each_item=False)
    def check_required_fields(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value

    @validator("referencetime")
    def check_referencetime(cls, values):
        return validate_time_range(values, "referencetime", "latest")

    @validator("geometry")
    def check_geoemtry(cls, values):
        if values != None:
            if validate_wkt(values):
                return values
            else:
                raise ValueError("geometry must be a WKT-string")

        return values


class LightningItem(BaseModel):
    Epoch: str
    Point: List[float]
    CloudIndicator: int
    PeakCurrentEstimate: int
    Multiplicity: int
    SolutionNOfSensors: int
    LocationDegreesOfFreedom: int
    EllipseAngle: float
    EllipseSemiMajorAxis: float
    EllipseSemiMinorAxis: float
    ChiSquare: float
    RiseTime: float
    PeakToZeroTime: float
    MaxRateOfRise: float
    AngleIndicator: int
    SignalIndicator: int
    TimingIndicator: int


class LightningResponse(RootModel):
    root: List[LightningItem]
