from typing import Any, Type

from frost.api import BaseReportEndpoint
from frost.client import BaseClient
from frost.entities import ReportWindrose
from frost.models import ReportWindroseRequest, ReportWindroseResponse


class ReportWindroseEndpoint(
    BaseReportEndpoint[ReportWindroseRequest, ReportWindroseResponse]
):
    request_model: Type[ReportWindroseRequest] = ReportWindroseRequest
    response_model: Type[ReportWindroseResponse] = ReportWindroseResponse
    report_type: str = "Windrose"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_report_windrose(self, **kwargs: Any) -> ReportWindrose:
        response_data: ReportWindroseResponse = self.get_data(**kwargs)
        return ReportWindrose(response_data)
