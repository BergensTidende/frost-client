from __future__ import annotations

from frost.api.base_endpoint import BaseEndpoint
from frost.entities.lightning import Lightning
from frost.models.lightning import LightningRequest, LightningResponse


class LightningEndpoint(BaseEndpoint):
    request_model = LightningRequest
    response_model = LightningResponse
    endpoint = "lightning"

    def get_lightning(
        self,
        **kwargs,
    ) -> Lightning | None:
        response_data = self.get_data(**kwargs)
        return Lightning(response_data)
