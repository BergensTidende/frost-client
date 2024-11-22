from __future__ import annotations

from typing import Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.entities import Observations
from frost.models import ObservationsRequest, ObservationsResponse


class ObservationsEndpoint(BaseEndpoint[ObservationsRequest, ObservationsResponse]):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_observations(self, **kwargs: Any) -> Optional[Observations]:
        # Force format to 'json' to ensure consistency
        kwargs["format"] = "json"
        response_data = self.get_data(**kwargs)

        if not response_data:
            print("No observations data available")
            return None

        # Ensure response_data is of type ObservationsResponse
        if isinstance(response_data, str):
            raise ValueError("Unexpected text response in ObservationsEndpoint")

        return Observations(response_data)
