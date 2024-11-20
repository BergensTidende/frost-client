from frost.api import BaseReportEndpoint
from frost.entities import ReportNormals
from frost.models import ReportNormalsRequest, ReportNormalsResponse


class ReportNormalsEndpoint(BaseReportEndpoint):
    request_model = ReportNormalsRequest
    response_model = ReportNormalsResponse
    report_type = "Normals"

    def get_report_normals(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportNormals(response_data)
