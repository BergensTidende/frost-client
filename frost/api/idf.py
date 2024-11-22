from __future__ import annotations

from typing import Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.entities import Idf
from frost.models import IdfRequest, IdfResponse


class IdfEndpoint(BaseEndpoint[IdfRequest, IdfResponse]):
    request_model = IdfRequest
    response_model = IdfResponse
    endpoint = "idf"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_idf(self, **kwargs: Any) -> Optional["Idf"]:
        kwargs["format"] = "json"
        response_data = self.get_data(**kwargs)

        if not response_data:
            print("No Idf data available")
            return None

        if isinstance(response_data, str):
            raise ValueError("Unexpected text response in IdfEndpoint")

        return Idf(response_data)
