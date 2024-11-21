from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.models import ObservationsRequest, ObservationsResponse

if TYPE_CHECKING:
    from frost.entities import Observations


class ObservationsEndpoint(BaseEndpoint):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_observations(self, **kwargs: Any) -> Optional[Observations]:
        response_data = self.get_data(**kwargs)
        return Observations(response_data)
