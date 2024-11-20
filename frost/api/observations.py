from __future__ import annotations

from typing import List, Optional

from frost.api import BaseEndpoint
from frost.entities import Observations
from frost.models import ObservationsRequest, ObservationsResponse
from frost.utils.arrays import array_to_param


class ObservationsEndpoint(BaseEndpoint):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def get_observations(self, **kwargs) -> Observations | None:
        response_data = self.get_data(**kwargs)
        return Observations(response_data)
