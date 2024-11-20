from __future__ import annotations

from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client.base_client import BaseClient
from frost.entities import ReportStationRecords
from frost.models import ReportStationRecordsRequest, ReportStationRecordsResponse


class ReportStationRecordsEndpoint(
    BaseReportEndpoint[ReportStationRecordsRequest, ReportStationRecordsResponse]
):
    request_model: Type[ReportStationRecordsRequest] = ReportStationRecordsRequest
    response_model: Type[ReportStationRecordsResponse] = ReportStationRecordsResponse
    report_type: str = "StationRecords"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_station_records(self, **kwargs: Any) -> ReportStationRecords:
        response_data: ReportStationRecordsResponse = self.get_data(**kwargs)
        return ReportStationRecords(response_data)
