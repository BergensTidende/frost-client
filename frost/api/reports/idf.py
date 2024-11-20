from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client.base_client import BaseClient
from frost.entities import ReportIdf
from frost.models import ReportIdfRequest, ReportIdfResponse


class ReportIdfEndpoint(BaseReportEndpoint[ReportIdfRequest, ReportIdfResponse]):
    request_model: Type[ReportIdfRequest] = ReportIdfRequest
    response_model: Type[ReportIdfResponse] = ReportIdfResponse
    report_type: str = "IDF"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_idf(self, **kwargs: Any) -> ReportIdf:
        response_data: ReportIdfResponse = self.get_data(**kwargs)
        return ReportIdf(response_data)
