from __future__ import annotations
from typing import List, Optional

from frost.utils.arrays import array_to_param


from frost.api.base_endpoint import BaseEndpoint
from frost.models.observations_models import ObservationsRequest, ObservationsResponse
from frost.entities.observations import Observations

class ObservationsEndpoint(BaseEndpoint):
    request_model = ObservationsRequest
    response_model = ObservationsResponse
    endpoint = "obs/met.no/filter"

    def get_observations(
        self,
        include_observations: bool = True,
        time: str = "latest",
        element_ids: Optional[str | List[str]] = None,
        location: Optional[str] = None,
        station_ids: Optional[str | List[str]] = None,
        nearest: Optional[str] = None,
        polygon: Optional[str] = None,
    ) -> Observations | None:
        """
        This form allows a dataset of time series type 'filter' to be
        downloaded from the Frost API

        To make a valid request, you must specify the when, where and what of the
        observation data you want: you must set the time parameter,
        an element type parameter and at least one station or (geo)location type
        parameter. Matching is case-insensitive, and you can use asterisks (*) for
        wildcard matching.

        :param bool include_observations: If you want to get weather observations set
        to True. If you only want information about the observations (metadata) set to
        False. Defaults to True
        :param str time: A time specification to select relevant observation times.
        Either a time range formated as "2020-01-01T00:00:00Z/2020-01-02T23:59:59Z",
        or the keyword latest can be used. By default if you use latest the
        maximum age of observations will be 3 hours, and only 1 latest observation will
        be returned. Defaults to "latest
        :param Optional[str  |  List[str]] element_ids: A comma-separated list of
        weather parameters. Use asterisk (*) for wildcard matching. Example: wind*,
        air_temperature. Defaults to None
        :param Optional[str] location: The country, county, municipality or place name
        of the weather observations. Use asterisk (*) for wildcard matching.
        Example: *stad,bergen, defaults to None
        :param Optional[str | List[str]] station_ids: A comma-separated list of internal
        MET Norway weather station ID numbers. Use asterisk (*) for wildcard matching.
        Example: 18700,55*, defaults to None
        :param Optional[str] nearest: A geographic search parameter to look for weather
        observations around a geographic point.
        Example: {"maxdist":7.5,"maxcount":3,"points":[{"lon":10.72,"lat":59.94}]},
        defaults to None
        :param Optional[str] polygon: A geographic search parameter to look for weather
        observations inside a geographic area (specifically a polygon).
        Example: [{"lat":59.93,"lon":10.05},{"lat":59.93,"lon":11},
        {"lat":60.25,"lon":10.77}], defaults to None
        :return Observations: Weather observations object
        """

        parameters = {
            "station_ids": array_to_param(station_ids),
            "include_observations": include_observations,
            "time": time,
        }

        if location is not None:
            parameters["location"] = time

        if element_ids is not None:
            parameters["elementids"] = array_to_param(element_ids)

        if nearest is not None:
            parameters["nearest"] = nearest

        if polygon is not None:
            parameters["polygon"] = polygon

        response_data = self.get_data(**parameters)
        return Observations(response_data)
