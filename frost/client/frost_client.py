from typing import List, Optional

from frost.api import (
    IdfAvailableEndpoint,
    IdfEndpoint,
    LightningEndpoint,
    ObservationsEndpoint,
    ReportDutEndpoint,
    ReportHumidityConstantsEndpoint,
    ReportIdfEndpoint,
    ReportNormalsEndpoint,
    ReportsAvailableEndpoint,
    ReportStationRecordsEndpoint,
    ReportTemperatureConstantsEndpoint,
    ReportWindroseEndpoint,
)
from frost.client import BaseClient
from frost.enteties import (
    Idf,
    IdfAvailable,
    Lightning,
    Observations,
    ReportDut,
    ReportHumidityConstants,
    ReportIdf,
    ReportNormals,
    ReportsAvailable,
    ReportStationRecords,
    ReportTemperatureConstants,
    ReportWindrose,
)
from frost.models import ScaleType
from frost.utils.array import array_to_param


class FrostClient(BaseClient):
    """Client for interacting with the Frost API.

    This class provides methods to retrieve observations from the Frost API.
    It serves as a wrapper around the ObservationsEndpoint, allowing users to easily
    make API calls to fetch observations.

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

    def get_observations(
        self,
        include_observations: bool = True,
        time: str = "latest",
        element_ids: Optional[str | List[str]] = None,
        location: Optional[str] = None,
        station_ids: Optional[str | List[str]] = None,
        nearest: Optional[str] = None,
        polygon: Optional[str] = None,
    ) -> Optional[Observations]:
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

        observations_endpoint = ObservationsEndpoint(self)
        return observations_endpoint.get_observations(**parameters)

    def get_lightning(
        self,
        reference_time: str = "latest",
        format: str = "json",
        geometry: Optional[str] = None,
    ) -> Optional[Lightning]:
        """Get lightning data, very very frightening
        Get lightning data from the MET Norway's data storage systems. The query
        parameters act as a filter; if all were left blank (not allowed in practice),
        one would retrieve all of the lightning data in the system.
        Restrict the data using the query parameters.

        :param str referenceTime: The time range to get observations for in either
                                  extended ISO-8601 format or the single word 'latest'.
        :param str format: the return format. Either json or ualf, defaults to "json"
        :param Optional[str] geometry: Get lightning within a polygon specified as
        POLYGON(...) using WKT; Example: POLYGON((4 60, 4 59, 6 59, 6 60, 4 60)),
        defaults to None

        :return Any: A list of lightning data
        """
        parameters = {
            "reference_time": reference_time,
            "format": format,
            "geometry": geometry,
        }

        lightning_endpoint = LightningEndpoint(self)
        return lightning_endpoint.get_lightning(**parameters)

    def get_idf_available(
        self, sources: Optional[str | List[str]] = None
    ) -> Optional[IdfAvailable]:
        """Get available IDF data
        Get available IDF data from the MET Norway's data storage systems. The query
        parameters act as a filter; if all were left blank (not allowed in practice),
        one would retrieve all of the IDF data in the system.
        Restrict the data using the query parameters.

        :param str referenceTime: The time range to get observations for in either
                                  extended ISO-8601 format or the single word 'latest'.
        :param str format: the return format. Either json or ualf, defaults to "json"
        :param Optional[str] geometry: Get IDF data within a polygon specified as
        POLYGON(...) using WKT; Example: POLYGON((4 60, 4 59, 6 59, 6 60, 4 60)),
        defaults to None

        :return Any: A list of IDF data
        """
        parameters = {}

        if sources is not None:
            sources = array_to_param(sources)
            parameters["sources"] = sources

        idf_available_endpoint = IdfAvailableEndpoint(self)
        return idf_available_endpoint.get_idf_available(**parameters)

    def get_idf(
        self,
        sources: Optional[str | List[str]] = None,
        location: Optional[str] = None,
        durations: Optional[str | List[str]] = None,
        frequencies: Optional[str | List[str]] = None,
        unit: Optional[str] = None,
    ) -> Optional[Idf]:
        """Get IDF data (intensity, duration, frequency) for requested combinations of
        sources, durations, frequencies, and (for a gridded IDF dataset)
        geographic location. The median intensity value (50th percentile) is
        accompanied with the 2.5 and 97.5 percentiles,
        i.e. the interval within which 95% of the intensity values are likely to be.


        :param Optional[str  |  List[str]] sources:
        The sources that you want IDF data for. Enter a comma-separated list of words
        where each word is either an integer for a station ID or 'grid' for the
        gridded dataset. By default, metadata from all available sources are returned.
        Defaults to None
        :param Optional[str] location: string location:
        The geographic position from which to get IDF data in case of a gridded dataset.
        Format: POINT(<longitude degrees> <latitude degrees>).
        Data from the nearest grid point are returned. Defaults to None
        :param Optional[str  |  List[str]] durations:
        The durations, in minutes, that you want IDF data for. Enter zero or
        more durations in a comma-separated list. By default, data for all available
        durations are returned. Defaults to None
        :param Optional[str  |  List[str]] frequencies:
        The frequencies (return periods), in years, that you want IDF data for.
        Enter zero or more frequencies in a comma-separated list. By default, data for
        all available frequencies are returned. Defaults to None
        :param Optional[str] unit:
        The unit of measure for the intensity. Specify 'mm' for millimetres per
        minute multiplied by the duration, or 'lsha' for litres per second per hectar.
        The default unit is 'lsha'. Defaults to None
        :return Idf | None: Returns the IDF data for the requested sources
        """
        parameters = {}

        if sources is not None:
            parameters["sources"] = array_to_param(sources)

        if durations is not None:
            parameters["durations"] = array_to_param(durations)

        if frequencies is not None:
            parameters["frequencies"] = array_to_param(frequencies)

        if location is not None:
            parameters["location"] = location

        if unit is not None:
            parameters["unit"] = unit

        idf_endpoint = IdfEndpoint(self)
        return idf_endpoint.get_idf(**parameters)

    def get_report_dut(self, source_id: str) -> Optional[ReportDut]:
        """Get DUT reports from the Frost API

        :param str source_id: The source id to get the report for
        :return ReportDut: The DUT report
        """
        parameters = {
            source_id: source_id,
        }

        report_dut_endpoint = ReportDutEndpoint(self)
        return report_dut_endpoint.get_report_dut(**parameters)

    def get_report_humidity_constants(
        self, source_id: str
    ) -> Optional[ReportHumidityConstants]:
        """Get humidity constants reports from the Frost API

        :param str source_id: The source id to get the report for
        :return ReportIdf | None: The ReportHumidityConstants object or None
        """
        parameters = {
            source_id: source_id,
        }

        report_humidity_constants_endpoint = ReportHumidityConstantsEndpoint(self)
        return report_humidity_constants_endpoint.get_humidity_constants(**parameters)

    def get_report_idf(self, station_id: int, unit: str) -> Optional[ReportIdf]:
        """Get IDF reports from the Frost API

        :param int station_id: The station id to get the report for
        :param str unit: The unit to get the report for. Available units are
        'mm', 'mm/h', 'mm/24h', 'mm/48h' or 'mm/72h'
        :return ReportIdf | None: The ReportIdf object or None
        """
        parameters = {
            "station_id": station_id,
            "unit": unit,
        }

        report_idf_endpoint = ReportIdfEndpoint(self)
        return report_idf_endpoint.get_report_idf(**parameters)

    def get_report_normals(
        self, element_id: str, period: str, station_id: int
    ) -> Optional[ReportNormals]:
        """_summary_

        :param str element_id: What element to get the report for
        :param str period: period of the report
        :param int station_id: station id to get the report for
        :raises APIError: if the request fails
        :return ReportNormals | None: Normals report object
        """
        parameters = {
            "element_id": element_id,
            "period": period,
            "station_id": station_id,
        }

        report_normals_endpoint = ReportNormalsEndpoint(self)
        return report_normals_endpoint.get_report_normals(**parameters)

    def get_report_station_records(
        self, station_id: int, record_category: str
    ) -> Optional[ReportStationRecords]:

        parameters = {
            "station_id": station_id,
            "record_category": record_category,
        }

        report_station_records_endpoint = ReportStationRecordsEndpoint(self)
        return report_station_records_endpoint.get_report_station_records(**parameters)

    def get_report_temperature_constants(
        self, station_id: int
    ) -> Optional[ReportTemperatureConstants]:

        parameters = {
            "station_id": station_id,
        }

        report_temperature_constants_endpoint = ReportTemperatureConstantsEndpoint(self)
        return report_temperature_constants_endpoint.get_report_temperature_constants(
            **parameters
        )

    def get_report_windrose(
        self,
        station_id: int,
        from_time: str,
        to_time: str,
        max_wind_speed: Optional[int] = None,
        months: Optional[List[int]] = None,
        scale: Optional[ScaleType] = None,
    ) -> Optional[ReportWindrose]:
        """Get windrose reports from the Frost API

        :param str settings: The serialized JSON object that contains the
        specification of a report of this type.
        :return Any: _description_
        """
        parameters = {
            "station_id": station_id,
            "from_time": from_time,
            "to_time": to_time,
        }

        if max_wind_speed is not None:
            parameters["Max_wind_speed"] = max_wind_speed

        if months is not None:
            parameters["Months"] = months

        if scale is not None:
            parameters["Scale"] = scale

        report_windrose_endpoint = ReportWindroseEndpoint(self)
        return report_windrose_endpoint.get_report_windrose(**parameters)

    def get_reports_available(
        self, type: Optional[str] = None
    ) -> Optional[ReportsAvailable]:
        """Get available reports from the Frost API

        :return Any: _description_
        """
        parameters = {
            "type": type,
        }

        reports_available_endpoint = ReportsAvailableEndpoint(self)
        return reports_available_endpoint.get_reports_available(**parameters)
