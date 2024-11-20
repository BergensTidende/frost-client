from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client.base_client import BaseClient
from frost.entities import ReportHumidityConstants
from frost.models import ReportHumidityConstantsRequest, ReportHumidityConstantsResponse


class ReportHumidityConstantsEndpoint(
    BaseReportEndpoint[ReportHumidityConstantsRequest, ReportHumidityConstantsResponse]
):
    request_model: Type[ReportHumidityConstantsRequest] = ReportHumidityConstantsRequest
    response_model: Type[
        ReportHumidityConstantsResponse
    ] = ReportHumidityConstantsResponse
    report_type: str = "HumidityConstants"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_humidity_constants(self, **kwargs: Any) -> ReportHumidityConstants:
        response_data: ReportHumidityConstantsResponse = self.get_data(**kwargs)
        return ReportHumidityConstants(response_data)
