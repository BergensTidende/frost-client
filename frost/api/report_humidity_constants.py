from pydantic import BaseModel, model_validator, List, Field

from .reports import ReportResponse


class ReportHumidityConstantsRequest(BaseModel):
    StationID: int

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if values.get("StationID") == None:
            raise ValueError("stationid must be provided")
        return values


# Failing for the moment with error {"error":"json.Unmarshal() failed: json:
# cannot unmarshal array into Go value of type map[string]interface {}"}
# observasjon@met.no


class FromTime(BaseModel):
    type: str


class ToTime(BaseModel):
    type: str


class Field1(BaseModel):
    type: str


class Field2(BaseModel):
    type: str


class Field3(BaseModel):
    type: str


class Field4(BaseModel):
    type: str


class Field5(BaseModel):
    type: str


class Field6(BaseModel):
    type: str


class Field7(BaseModel):
    type: str


class Field8(BaseModel):
    type: str


class Field9(BaseModel):
    type: str


class Field10(BaseModel):
    type: str


class Field11(BaseModel):
    type: str


class Field12(BaseModel):
    type: str


class ValueProperties(BaseModel):
    field_1: Field1 = Field(..., alias="1")
    field_2: Field2 = Field(..., alias="2")
    field_3: Field3 = Field(..., alias="3")
    field_4: Field4 = Field(..., alias="4")
    field_5: Field5 = Field(..., alias="5")
    field_6: Field6 = Field(..., alias="6")
    field_7: Field7 = Field(..., alias="7")
    field_8: Field8 = Field(..., alias="8")
    field_9: Field9 = Field(..., alias="9")
    field_10: Field10 = Field(..., alias="10")
    field_11: Field11 = Field(..., alias="11")
    field_12: Field12 = Field(..., alias="12")


class Values(BaseModel):
    properties: ValueProperties
    type: str


class Properties(BaseModel):
    from_time: FromTime = Field(..., alias="FromTime")
    to_time: ToTime = Field(..., alias="ToTime")
    values: Values = Field(..., alias="Values")


class Items(BaseModel):
    properties: Properties
    required: List[str]
    type: str


class HumidityConstants(BaseModel):
    items: Items
    type: str


class ReportHumidityConstantsResponse(ReportResponse[HumidityConstants]):
    pass
