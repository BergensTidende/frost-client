from frost.client.base_client import BaseClient
from frost.api.observations import ObservationsEndpoint


class FrostClient(BaseClient):
    """Client for interacting with the Frost API.

    This class provides methods to retrieve observations from the Frost API.
    It serves as a wrapper around the ObservationsEndpoint, allowing users to easily make API calls to fetch observations.

    Args:
        **kwargs: Additional keyword arguments to customize the API request.

    Returns:
        The response from the API containing the requested observations.

    Raises:
        Any exceptions raised by the ObservationsEndpoint during the API call.

    Examples:
        client = FrostClient()
        observations = client.get_observations(param1=value1, param2=value2)
    """

    def get_observations(self, **kwargs):
        """Retrieve observations from the Frost API.

        This method interacts with the ObservationsEndpoint to fetch observations based
        on the provided parameters.

        It allows users to customize their request through keyword arguments.

        Args:
            **kwargs: Additional keyword arguments to customize the API request.

        Returns:
            The response from the API containing the requested observations.

        Raises:
            Any exceptions raised by the ObservationsEndpoint during the API call.

        Examples:
            observations = client.get_observations(param1=value1, param2=value2)
        """
        observations_endpoint = ObservationsEndpoint(self)
        return observations_endpoint.get_observations(**kwargs)
