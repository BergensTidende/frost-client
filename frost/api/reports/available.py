from __future__ import annotations

from typing import Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.entities import ReportsAvailable
from frost.models import ReportsAvailableRequest, ReportsAvailableResponse


class ReportsAvailableEndpoint(
    BaseEndpoint[ReportsAvailableRequest, ReportsAvailableResponse]
):
    request_model = ReportsAvailableRequest
    response_model = ReportsAvailableResponse
    report_type = "reports/available"

    def __init__(self, client: BaseClient):
        super().__init__(client)

    def get_reports_available(self, **kwargs: Any) -> Optional["ReportsAvailable"]:
        kwargs["format"] = "json"
        response_data = self.get_data(**kwargs)

        if not response_data:
            print("No Idf data available")
            return None

        if isinstance(response_data, str):
            raise ValueError("Unexpected text response in ReportsAvailableEndpoint")

        return ReportsAvailable(response_data)
