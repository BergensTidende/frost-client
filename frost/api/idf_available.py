from frost.api.base_endpoint import BaseEndpoint
from frost.entities.observations import Observations
from frost.models.observations import ObservationsRequest, ObservationsResponse


class IdfAvailableEndpoint(BaseEndpoint):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def get_idf_available(self, **kwargs):
        response_data = self.get_data(**kwargs)
        return Observations(response_data)
