from typing import List

from pydantic import BaseModel, model_validator, Field

from .reports import ReportResponse


class ReportStationRecordsRequest(BaseModel):
    StationID: int
    RecordCategory: str

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if values.get("StationID") == None & values.get("RecordCategory") == None:
            raise ValueError("Both StationID and RecordCategory must be provided")
        return values


class Label(BaseModel):
    type: str


class ObsTime(BaseModel):
    type: str


class TimeSeriesId(BaseModel):
    type: str


class InstancesProperties(BaseModel):
    label: Label
    obs_time: ObsTime = Field(..., alias="obsTime")
    time_series_id: TimeSeriesId = Field(..., alias="timeSeriesID")


class InstancesItems(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: InstancesProperties
    required: List[str]
    type: str


class Instances(BaseModel):
    items: InstancesItems
    min_items: int = Field(..., alias="minItems")
    type: str


class Order(BaseModel):
    type: str


class RecordFrom(BaseModel):
    type: str


class RecordTo(BaseModel):
    type: str


class Value(BaseModel):
    type: str


class RecordChronologyProperties(BaseModel):
    instances: Instances
    label: Label
    order: Order
    record_from: RecordFrom = Field(..., alias="recordFrom")
    record_to: RecordTo = Field(..., alias="recordTo")
    value: Value


class RecordChronologyItems(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: RecordChronologyProperties
    required: List[str]
    type: str


class RecordChronology(BaseModel):
    items: RecordChronologyItems
    type: str


class Alltime(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field01(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field02(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field03(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field04(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field05(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field06(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field07(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field08(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field09(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field10(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field11(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Field12(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class MonthsProperties(BaseModel):
    field_01: Field01 = Field(..., alias="01")
    field_02: Field02 = Field(..., alias="02")
    field_03: Field03 = Field(..., alias="03")
    field_04: Field04 = Field(..., alias="04")
    field_05: Field05 = Field(..., alias="05")
    field_06: Field06 = Field(..., alias="06")
    field_07: Field07 = Field(..., alias="07")
    field_08: Field08 = Field(..., alias="08")
    field_09: Field09 = Field(..., alias="09")
    field_10: Field10 = Field(..., alias="10")
    field_11: Field11 = Field(..., alias="11")
    field_12: Field12 = Field(..., alias="12")


class Months(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: MonthsProperties
    type: str


class RecordMonthsProperties(BaseModel):
    alltime: Alltime
    months: Months


class RecordMonths(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: RecordMonthsProperties
    type: str


class FieldDefs(BaseModel):
    record_chronology: RecordChronology = Field(..., alias="recordChronology")
    record_months: RecordMonths = Field(..., alias="recordMonths")


class Days(BaseModel):
    type: str


class LongestGapSeconds(BaseModel):
    type: str


class Months1(BaseModel):
    type: str


class ValueCount(BaseModel):
    type: str


class Years(BaseModel):
    type: str


class DataCoverageProperties(BaseModel):
    days: Days
    longest_gap_seconds: LongestGapSeconds = Field(..., alias="longestGapSeconds")
    months: Months1
    value_count: ValueCount = Field(..., alias="valueCount")
    years: Years


class DataCoverage(BaseModel):
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: DataCoverageProperties
    required: List[str]
    type: str


class Max(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class Min(BaseModel):
    field_ref: str = Field(..., alias="$ref")


class MeasurementPeriodsItemsItems(BaseModel):
    type: str


class MeasurementPeriodsItems(BaseModel):
    items: MeasurementPeriodsItemsItems
    max_items: int = Field(..., alias="maxItems")
    min_items: int = Field(..., alias="minItems")
    type: str


class MeasurementPeriods(BaseModel):
    items: MeasurementPeriodsItems
    min_items: int = Field(..., alias="minItems")
    type: str


class RecordCategory(BaseModel):
    type: str


class StationId(BaseModel):
    type: str


class UpdatedFullScan(BaseModel):
    type: str


class UpdatedIncremental(BaseModel):
    type: str


class Properties(BaseModel):
    data_coverage: DataCoverage = Field(..., alias="dataCoverage")
    max: Max
    measurement_periods: MeasurementPeriods = Field(..., alias="measurementPeriods")
    min: Min
    record_category: RecordCategory = Field(..., alias="recordCategory")
    station_id: StationId = Field(..., alias="stationID")
    updated_full_scan: UpdatedFullScan = Field(..., alias="updatedFullScan")
    updated_incremental: UpdatedIncremental = Field(..., alias="updatedIncremental")


class StationRecords(BaseModel):
    field_defs: FieldDefs = Field(..., alias="$defs")
    additional_properties: bool = Field(..., alias="additionalProperties")
    properties: Properties
    required: List[str]
    type: str


class ReportStationRecordsResponse(ReportResponse[StationRecords]):
    pass
