from frost.api import BaseEndpoint
from frost.entities import Idf
from frost.models import IdfRequest, IdfResponse


class IdfEndpoint(BaseEndpoint):
    request_model = IdfRequest
    response_model = IdfResponse
    endpoint = "idf"

    def get_idf(self, **kwargs) -> Idf | None:
        response_data = self.get_data(**kwargs)
        return Idf(response_data)
