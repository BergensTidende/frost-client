from typing import List, Optional

from pydantic import BaseModel, model_validator, validator, Field

from frost.utils.validation import validate_time

from .reports import ScaleType, ReportResponse


class ReportWindroseRequest(BaseModel):
    StationID: str
    FromTime: str
    ToTime: str
    Months: Optional[List[int]] = None
    MaxWindSpeed: Optional[int] = None
    Scale: Optional[ScaleType] = None

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if (
            values.get("StationID")
            == None & values.get("FromTime")
            == None & values.get("ToTime")
            == None
        ):
            raise ValueError("Both StationID, FromTime and ToTime must be provided")
        return values

    @validator("FromTime")
    def check_valid_from_time(cls, values):
        return validate_time(values, "FromTime")

    @validator("ToTime")
    def check_valid_to_time(cls, values):
        return validate_time(values, "ToTime")


class Title(BaseModel):
    type: str


class Value(BaseModel):
    type: str


class ExtrasItemsProperties(BaseModel):
    title: Title
    value: Value


class ExtrasItems(BaseModel):
    properties: ExtrasItemsProperties
    required: List[str]
    type: str


class Extras(BaseModel):
    items: ExtrasItems
    type: str


class Name(BaseModel):
    type: str


class TypeItems(BaseModel):
    type: str


class Sums(BaseModel):
    items: TypeItems
    type: str


class Titles(BaseModel):
    items: TypeItems
    type: str


class HorizontalAxisProperties(BaseModel):
    name: Name
    sums: Sums
    titles: Titles


class HorizontalAxis(BaseModel):
    properties: HorizontalAxisProperties
    required: List[str]
    type: str


class AutomaticData(BaseModel):
    items: TypeItems
    type: str


class FromTime(BaseModel):
    type: str


class ManualData(BaseModel):
    items: TypeItems
    type: str


class Months(BaseModel):
    items: TypeItems
    type: str


class NumberOfValues(BaseModel):
    type: str


class StationId(BaseModel):
    type: str


class ToTime(BaseModel):
    type: str


class MetadataProperties(BaseModel):
    automatic_data: AutomaticData = Field(..., alias="automaticData")
    from_time: FromTime = Field(..., alias="fromTime")
    manual_data: ManualData = Field(..., alias="manualData")
    months: Months
    number_of_values: NumberOfValues = Field(..., alias="numberOfValues")
    station_id: StationId = Field(..., alias="stationID")
    to_time: ToTime = Field(..., alias="toTime")


class Metadata(BaseModel):
    properties: MetadataProperties
    required: List[str]
    type: str


class TableItems(BaseModel):
    items: TypeItems
    type: str


class Table(BaseModel):
    items: TableItems
    type: str


class SumsTitlesItems(BaseModel):
    type: str

class VerticalAxisProperties(BaseModel):
    name: Name
    sums: Sums
    titles: Titles


class VerticalAxis(BaseModel):
    properties: VerticalAxisProperties
    required: List[str]
    type: str


class Properties(BaseModel):
    extras: Extras
    horizontal_axis: HorizontalAxis = Field(..., alias="horizontalAxis")
    metadata: Metadata
    table: Table
    vertical_axis: VerticalAxis = Field(..., alias="verticalAxis")


class WindRose(BaseModel):
    properties: Properties
    required: List[str]
    type: str


class ReportWindroseResponse(ReportResponse[WindRose]):
    pass
