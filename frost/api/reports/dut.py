from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client.base_client import BaseClient
from frost.entities import ReportDut
from frost.models import ReportDutRequest, ReportDutResponse


class ReportDutEndpoint(BaseReportEndpoint[ReportDutRequest, ReportDutResponse]):
    request_model: Type[ReportDutRequest] = ReportDutRequest
    response_model: Type[ReportDutResponse] = ReportDutResponse
    report_type: str = "DUT"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_dut(self, **kwargs: Any) -> ReportDut:
        response_data: ReportDutResponse = self.get_data(**kwargs)
        return ReportDut(response_data)
