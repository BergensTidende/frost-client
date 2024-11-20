from frost.api import BaseReportEndpoint
from frost.entities import ReportStationRecords
from frost.models import ReportStationRecordsRequest, ReportStationRecordsResponse


class ReportStationRecordsEndpoint(BaseReportEndpoint):
    request_model = ReportStationRecordsRequest
    response_model = ReportStationRecordsResponse
    report_type = "StationRecords"

    def get_report_station_records(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportStationRecords(response_data)
