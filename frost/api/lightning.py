from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, model_validator, validator

from frost.utils.validation import validate_time_range, validate_wkt

class FormatType(str, Enum):
    json = "json"
    ualf = "ualf"

class LightningRequest(BaseModel):
    referencetime: str
    format: FormatType
    geometry: Optional[str] = None

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if values.get("referencetime") == None & values.get("format") == None:
            raise ValueError("Both referencetime and format must be provided")
        return values

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


class LightningResponse(BaseModel):
    __root__: List[LightningItem]
