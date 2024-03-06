from typing import List, Optional

from pydantic import BaseModel, field_validator, Field


class ReportStationRecordsRequest(BaseModel):
    station_id: int = Field(None, alias="StationID")
    record_category: str = Field(None, alias="RecordCategory")

    class Config:
        populate_by_name = True

    @field_validator("station_id", "record_category")
    def check_required_fields(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} must be provided")
        return value


class Instance(BaseModel):
    label: str
    obsTime: str
    timeSeriesID: int


class Item(BaseModel):
    instances: List[Instance]
    order: int
    record_from: str = Field(..., alias="recordFrom")
    record_to: Optional[str] = Field(None, alias="recordTo")
    value: float | int


class Months(BaseModel):
    field_10: List[Item] = Field(..., alias="10")
    field_11: List[Item] = Field(..., alias="11")
    field_12: List[Item] = Field(..., alias="12")
    field_01: List[Item] = Field(..., alias="01")
    field_02: List[Item] = Field(..., alias="02")
    field_03: List[Item] = Field(..., alias="03")
    field_04: List[Item] = Field(..., alias="04")
    field_05: List[Item] = Field(..., alias="05")
    field_06: List[Item] = Field(..., alias="06")
    field_07: List[Item] = Field(..., alias="07")
    field_08: List[Item] = Field(..., alias="08")
    field_09: List[Item] = Field(..., alias="09")


class MinMax(BaseModel):
    alltime: List[Item]
    months: Months


class DataCoverage(BaseModel):
    days: Optional[int]
    longest_gap_seconds: int = Field(..., alias="longestGapSeconds")
    months: int
    value_count: int = Field(..., alias="valueCount")
    years: int


class ReportStationRecordsResponse(BaseModel):
    data_coverage: DataCoverage = Field(..., alias="dataCoverage")
    max: MinMax
    min: MinMax
    measurement_periods: List[List[str]] = Field(..., alias="measurementPeriods")
    record_category: str = Field(..., alias="recordCategory")
    station_id: int = Field(..., alias="stationID")
    updated_full_scan: str = Field(..., alias="updatedFullScan")
    updated_incremental: str = Field(..., alias="updatedIncremental")
