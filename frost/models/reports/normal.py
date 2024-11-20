from pydantic import BaseModel, model_validator

from .reports import ReportResponse

class NormalsReportRequest(BaseModel):
    ElementID: str
    Period: str
    StationID: int

    @model_validator(mode="before")
    def check_required_fields(cls, values):
        if (
            values.get("ElementID")
            == None & values.get("Period")
            == None & values.get("StationID")
            == None
        ):
            raise ValueError("Both ElementID, Period and StationID must be provided")
        return values

class Normals(BaseModel):
    ElementID: str
    Period: str
    StationID: int
    Unit: str
    Value: float

class NormalReportResponse(ReportResponse[Normal]):
    pass
