from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from enum import Enum

DataT = TypeVar('DataT')

class ScaleType(str, Enum):
    beaufort = 'beaufort'
    meters_per_second = 'm/s'

class ReportRequest(BaseModel):
    type: str
    settings: dict

class ReportResponse(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
