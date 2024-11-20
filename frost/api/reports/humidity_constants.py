from frost.api import BaseReportEndpoint
from frost.entities import ReportHumidityConstants
from frost.models import ReportHumidityConstantsRequest, ReportHumidityConstantsResponse


class ReportHumidityConstantsEndpoint(BaseReportEndpoint):
    request_model = ReportHumidityConstantsRequest
    response_model = ReportHumidityConstantsResponse
    report_type = "HumidityConstants"

    def get_humidity_constants(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportHumidityConstants(response_data)
