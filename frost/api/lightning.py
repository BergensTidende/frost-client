from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from frost.api.base_endpoint import BaseEndpoint
from frost.client import BaseClient
from frost.models.lightning import LightningRequest, LightningResponse

if TYPE_CHECKING:
    from frost.entities import Lightning


class LightningEndpoint(BaseEndpoint):
    request_model = LightningRequest
    response_model = LightningResponse
    endpoint = "lightning"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_lightning(
        self,
        **kwargs: Any,
    ) -> Optional[Lightning]:
        response_data = self.get_data(**kwargs)
        return Lightning(response_data)
