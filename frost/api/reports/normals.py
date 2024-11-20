from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client import BaseClient
from frost.entities import ReportNormals
from frost.models import ReportNormalsRequest, ReportNormalsResponse


class ReportNormalsEndpoint(
    BaseReportEndpoint[ReportNormalsRequest, ReportNormalsResponse]
):
    request_model: Type[ReportNormalsRequest] = ReportNormalsRequest
    response_model: Type[ReportNormalsResponse] = ReportNormalsResponse
    report_type: str = "Normals"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_normals(self, **kwargs: Any) -> ReportNormals:
        response_data: ReportNormalsResponse = self.get_data(**kwargs)
        return ReportNormals(response_data)
