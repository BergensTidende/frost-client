from frost.api import BaseEndpoint
from frost.entities import ReportsAvailable
from frost.models import ReportsAvailableRequest, ReportsAvailableResponse


class ReportsAvailableEndpoint(BaseEndpoint):
    request_model = ReportsAvailableRequest
    response_model = ReportsAvailableResponse
    report_type = "reports/available"

    def get_reports_available(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportsAvailable(response_data)
