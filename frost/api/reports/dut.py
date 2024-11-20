from frost.api import BaseReportEndpoint
from frost.entities import ReportDut
from frost.models import ReportDutRequest, ReportDutResponse


class ReportDutEndpoint(BaseReportEndpoint):
    request_model = ReportDutRequest
    response_model = ReportDutResponse
    report_type = "DUT"

    def get_report_dut(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportDut(response_data)
