from __future__ import annotations

from typing import Any, Dict, Generic, TypeVar

from pydantic import BaseModel

from frost.api.base_endpoint import BaseEndpoint
from frost.client.base_client import BaseClient

# Define type variables for request and response models
RequestType = TypeVar("RequestType", bound=BaseModel)
ResponseType = TypeVar("ResponseType", bound=BaseModel)


class BaseReportEndpoint(BaseEndpoint, Generic[RequestType, ResponseType]):
    report_type: str  # Each report will specify its type

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_data(self, **kwargs: Any) -> ResponseType:
        # The request model is expected to be the settings for the report
        params: Dict[str, Any] = self.validate_request(**kwargs)
        # For reports, the 'settings' parameter is a JSON string
        settings_json: str = params.get("settings", "{}")

        request_params: Dict[str, Any] = {
            "type": self.report_type,
            "settings": settings_json,
        }

        response_json: Dict[str, Any] = self.client.make_request(
            "reports", request_params
        )
        return self.validate_response(response_json)
