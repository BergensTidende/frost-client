from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, field_validator, ValidationInfo

DataT = TypeVar("DataT")


class ScaleType(str, Enum):
    beaufort = "beaufort"
    meters_per_second = "m/s"


class FormatType(str, Enum):
    json = "json"
    ualf = "ualf"


class ReportRequest(BaseModel):
    type: str
    settings: str

    @field_validator("type", "settings")
    @classmethod
    def check_required_fields(cls, value: str, info: ValidationInfo):
        if value is None:
            raise ValueError(f"{info.field_name} must be provided")

        return value


class ReportResponse(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
