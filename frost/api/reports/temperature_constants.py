from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client import BaseClient
from frost.entities import ReportTemperatureConstants
from frost.models import (
    ReportTemperatureConstantsRequest,
    ReportTemperatureConstantsResponse,
)


class ReportTemperatureConstantsEndpoint(
    BaseReportEndpoint[
        ReportTemperatureConstantsRequest, ReportTemperatureConstantsResponse
    ]
):
    request_model: Type[
        ReportTemperatureConstantsRequest
    ] = ReportTemperatureConstantsRequest
    response_model: Type[
        ReportTemperatureConstantsResponse
    ] = ReportTemperatureConstantsResponse
    report_type: str = "TemperatureConstants"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_temperature_constants(
        self, **kwargs: Any
    ) -> ReportTemperatureConstants:
        response_data: ReportTemperatureConstantsResponse = self.get_data(**kwargs)
        return ReportTemperatureConstants(response_data)
