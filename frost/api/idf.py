from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from frost.api import BaseEndpoint
from frost.client import BaseClient
from frost.models import IdfRequest, IdfResponse

if TYPE_CHECKING:
    from frost.entities import Idf


class IdfEndpoint(BaseEndpoint):
    request_model = IdfRequest
    response_model = IdfResponse
    endpoint = "idf"

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)

    def get_idf(self, **kwargs: Any) -> Optional["Idf"]:
        response_data = self.get_data(**kwargs)
        return Idf(response_data)
