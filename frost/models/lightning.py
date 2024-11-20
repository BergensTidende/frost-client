from typing import List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator, ValidationInfo

from frost.utils.validation import validate_time_range, validate_wkt

from .reports import FormatType


class LightningRequest(BaseModel):
    reference_time: str = Field(..., alias="referencetime")
    format: FormatType
    geometry: Optional[str] = None

    @field_validator("reference_time", "format")
    @classmethod
    def check_required_fields(cls, value: str, info: ValidationInfo):
        if value is None:
            raise ValueError(f"{info.field_name} must be provided")
        return value

    @field_validator("reference_time")
    @classmethod
    def check_referencetime(cls, values: str, info: ValidationInfo):
        return validate_time_range(values, info.field_name, "latest")

    @field_validator("geometry")
    @classmethod
    def check_geoemtry(cls, values: str, info: ValidationInfo):
        if values is not None:
            if validate_wkt(values):
                return values
            else:
                raise ValueError(f"{info.field_name} must be a WKT-string")

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
