from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator

from frost.utils.validation import validate_time_range, validate_wkt

from .report import FormatType
from .ualf import Ualf


class LightningRequest(BaseModel):
    reference_time: str = Field(..., alias="referencetime")
    format: FormatType
    geometry: Optional[str] = None

    @field_validator("reference_time")
    @classmethod
    def check_referencetime(cls, value: str) -> str:
        # Example logic for validating 'reference_time', including 'latest' as valid
        if value != "latest" and not validate_time_range(value, "reference_time"):
            raise ValueError("Invalid reference time format.")
        return value

    @field_validator("geometry")
    @classmethod
    def check_geometry(cls, value: Optional[str]) -> Optional[str]:
        if value and not validate_wkt(value):
            raise ValueError("Geometry must be a valid WKT string.")
        return value


class LightningItem(BaseModel):
    Epoch: str
    Point: List[float]
    CloudIndicator: int
    PeakCurrentEstimate: int = Field(..., alias="peak_current")
    Multiplicity: int
    SolutionNOfSensors: int = Field(..., alias="number_of_sensors")
    LocationDegreesOfFreedom: int = Field(..., alias="degrees_of_freedom")
    EllipseAngle: float = Field(..., alias="ellipse_angle")
    EllipseSemiMajorAxis: float = Field(..., alias="semi_major_axis")
    EllipseSemiMinorAxis: float = Field(..., alias="semi_minor_axis")
    ChiSquare: float = Field(..., alias="chi_square_value")
    RiseTime: float = Field(..., alias="rise_time")
    PeakToZeroTime: float = Field(..., alias="peak_to_zero_time")
    MaxRateOfRise: float = Field(..., alias="max_rate_of_rise")
    AngleIndicator: int = Field(..., alias="angle_indicator")
    SignalIndicator: int = Field(..., alias="signal_indicator")
    TimingIndicator: int = Field(..., alias="timing_indicator")

    class Config:
        allow_population_by_alias = True
        populate_by_name = True


class LightningResponse(RootModel[List[LightningItem]]):
    pass

    @classmethod
    def from_ualf(cls, ualf_text: str) -> "LightningResponse":
        """
        Parse UALF text data into a LightningResponse object.
        """
        lines = ualf_text.strip().split("\n")
        items = []

        for line in lines:
            if not line.strip():
                continue  # Skip empty lines

            try:
                ualf = Ualf(line)
                parsed = ualf.parse()
                items.append(LightningItem(**parsed))
                print("created item")
            except Exception as e:
                print(f"Error parsing UALF line: {parsed}, Error: {e}")

        return cls.model_validate(items)
