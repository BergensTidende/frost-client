from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator

from frost.utils.validation import validate_time_range, validate_wkt

from .report import FormatType


class LightningRequest(BaseModel):
    reference_time: str = Field(..., alias="referencetime")
    format: FormatType
    geometry: Optional[str] = None

    @field_validator("reference_time", "format")
    def check_required_fields(cls, value: Any, info: Any) -> Any:
        # 'info' is typed as 'Any' due to incomplete type hints in Pydantic
        if value is None:
            field_name = getattr(info, "field_name", "unknown")
            raise ValueError(f"{field_name} must be provided")
        return value

    @field_validator("reference_time")
    def check_referencetime(cls, value: str, info: Any) -> str:
        # 'info' is typed as 'Any' due to incomplete type hints in Pydantic
        field_name = getattr(info, "field_name", "")
        return validate_time_range(value, field_name, "latest")

    @field_validator("geometry")
    def check_geometry(cls, value: Optional[str], info: Any) -> Optional[str]:
        # 'info' is typed as 'Any' due to incomplete type hints in Pydantic
        if value is not None:
            if validate_wkt(value):
                return value
            field_name = getattr(info, "field_name", "unknown")
            raise ValueError(f"{field_name} must be a WKT-string")
        return value


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
