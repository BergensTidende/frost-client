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
    @classmethod
    def from_ualf(cls, ualf_text: str) -> "LightningResponse":
        """
        Parse UALF text data into a LightningResponse object.
        """
        lines = ualf_text.strip().split("\n")
        items = []

        for line in lines:
            try:
                ualf = Ualf(line)
                parsed = ualf.parse()
                items.append(
                    LightningItem(
                        Epoch=f"{parsed['year']}-{parsed['month']:02}-{parsed['day']:02}T{parsed['hour']:02}:{parsed['minutes']:02}:{parsed['seconds']:02}Z",  # noqa: E501
                        Point=[parsed["latitude"], parsed["longitude"]],
                        CloudIndicator=parsed["cloud_indicator"],
                        PeakCurrentEstimate=parsed["peak_current"],
                        Multiplicity=parsed["multiplicity"],
                        SolutionNOfSensors=parsed["number_of_sensors"],
                        LocationDegreesOfFreedom=parsed["degrees_of_freedom"],
                        EllipseAngle=parsed["ellipse_angle"],
                        EllipseSemiMajorAxis=parsed["semi_major_axis"],
                        EllipseSemiMinorAxis=parsed["semi_minor_axis"],
                        ChiSquare=parsed["chi_square_value"],
                        RiseTime=parsed["rise_time"],
                        PeakToZeroTime=parsed["peak_to_zero_time"],
                        MaxRateOfRise=parsed["max_rate_of_rise"],
                        AngleIndicator=parsed["angle_indicator"],
                        SignalIndicator=parsed["signal_indicator"],
                        TimingIndicator=parsed["timing_indicator"],
                    )
                )
            except Exception as e:
                print(f"Error parsing UALF line: {line}, Error: {e}")

        return cls(root=items)
