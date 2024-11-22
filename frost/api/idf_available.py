from __future__ import annotations

from typing import Any, Optional

from frost.api.base_endpoint import BaseEndpoint
from frost.client import BaseClient
from frost.entities import IdfAvailable
from frost.models import IdfAvailableRequest, IdfAvailableResponse


class IdfAvailableEndpoint(BaseEndpoint[IdfAvailableRequest, IdfAvailableResponse]):
    request_model = IdfAvailableRequest
    response_model = IdfAvailableResponse
    endpoint = "idf/available"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_idf_available(self, **kwargs: Any) -> Optional["IdfAvailable"]:
        kwargs["format"] = "json"
        response_data = self.get_data(**kwargs)

        if not response_data:
            print("No IdfAvailable data available")
            return None

        if isinstance(response_data, str):
            raise ValueError("Unexpected text response in IdfAvailableEndpoint")

        return IdfAvailable(response_data)
