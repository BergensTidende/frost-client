from frost.api import BaseReportEndpoint
from frost.entities import ReportTemperatureConstants
from frost.models import (
    ReportTemperatureConstantsRequest,
    ReportTemperatureConstantsResponse,
)


class ReportTemperatureConstantsEndpoint(BaseReportEndpoint):
    request_model = ReportTemperatureConstantsRequest
    response_model = ReportTemperatureConstantsResponse
    report_type = "TemperatureConstants"

    def get_report_temperature_constants(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportTemperatureConstants(response_data)
