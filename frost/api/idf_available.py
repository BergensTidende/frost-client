from __future__ import annotations

from typing import Any, Optional

from frost.api.base_endpoint import BaseEndpoint
from frost.client import BaseClient
from frost.entities.observations import Observations
from frost.models.observations import ObservationsRequest, ObservationsResponse


class IdfAvailableEndpoint(BaseEndpoint):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_idf_available(self, **kwargs: Any) -> Optional[Observations]:
        response_data = self.get_data(**kwargs)
        return Observations(response_data)
