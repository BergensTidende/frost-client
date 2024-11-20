from frost.api import BaseReportEndpoint
from frost.entities import ReportIdf
from frost.models import ReportIdfRequest, ReportIdfResponse


class ReportIdfEndpoint(BaseReportEndpoint):
    request_model = ReportIdfRequest
    response_model = ReportIdfResponse
    report_type = "IDF"

    def get_report_idf(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportIdf(response_data)
