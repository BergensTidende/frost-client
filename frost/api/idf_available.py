from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from frost.api.base_endpoint import BaseEndpoint
from frost.client import BaseClient
from frost.models import IdfAvailableRequest, IdfAvailableResponse

if TYPE_CHECKING:
    from frost.entities import IdfAvailable


class IdfAvailableEndpoint(BaseEndpoint):
    request_model = IdfAvailableRequest
    response_model = IdfAvailableResponse
    endpoint = "idf/available"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_idf_available(self, **kwargs: Any) -> Optional["IdfAvailable"]:
        response_data = self.get_data(**kwargs)
        return IdfAvailable(response_data)
