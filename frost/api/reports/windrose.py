from frost.api import BaseReportEndpoint
from frost.entities import ReportWindrose
from frost.models import ReportWindroseRequest, ReportWindroseResponse


class ReportWindroseEndpoint(BaseReportEndpoint):
    request_model = ReportWindroseRequest
    response_model = ReportWindroseResponse
    report_type = "Windrose"

    def get_report_windrose(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return ReportWindrose(response_data)
