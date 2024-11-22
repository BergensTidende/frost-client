from __future__ import annotations

from typing import Any, Optional

from frost.api.base_endpoint import BaseEndpoint
from frost.client import BaseClient
from frost.entities import Lightning
from frost.models.lightning import LightningRequest, LightningResponse


class LightningEndpoint(BaseEndpoint[LightningRequest, LightningResponse]):
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

        if not response_data:
            print("No lightning data available")
            return None

        # Check format and process accordingly
        if kwargs.get("format") == "ualf":
            # Parse UALF and convert to Lightning entity
            if not isinstance(response_data, str):
                raise ValueError("Expected raw UALF text for 'ualf' format")
            lightning_response = LightningResponse.from_ualf(
                response_data
            )  # response_data should be str here
        elif isinstance(response_data, LightningResponse):
            lightning_response = response_data
        else:
            raise ValueError("Expected a LightningResponse object for JSON format")

        # Convert the response into a Lightning entity
        return Lightning(lightning_response)
