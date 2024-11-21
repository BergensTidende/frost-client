from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.models import ReportsAvailableRequest, ReportsAvailableResponse

if TYPE_CHECKING:
    from frost.entities import ReportsAvailable


class ReportsAvailableEndpoint(BaseEndpoint):
    request_model = ReportsAvailableRequest
    response_model = ReportsAvailableResponse
    report_type = "reports/available"

    def __init__(self, client: BaseClient):
        super().__init__(client)

    def get_reports_available(self, **kwargs: Any) -> Optional["ReportsAvailable"]:
        response_data = self.get_data(**kwargs)
        return ReportsAvailable(response_data)
