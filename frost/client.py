from __future__ import annotations

import json
from os import getenv
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from pydantic import ValidationError

from frost.api import (
    IdfRequest,
    IdfAvailableRequest,
    LightningRequest,
    ObservationsRequest,
    ReportRequest,
    ReportDutRequest,
    ReportHumidityConstantsRequest,
    ReportIdfRequest,
    ReportNormalsRequest,
    ReportStationRecordsRequest,
    ReportTemperatureConstantsRequest,
    ReportWindroseRequest,
    ReportsAvailableRequest,
    ScaleType,
    IdfResponse,
    IdfAvailableResponse,
    LightningResponse,
    ObservationsResponse,
    ReportResponse,
    ReportDutResponse,
    ReportHumidityConstantsResponse,
    ReportIdfResponse,
    ReportNormalsResponse,
    ReportStationRecordsResponse,
    ReportTemperatureConstantsResponse,
    ReportWindroseResponse,
    ReportsAvailableResponse,
)
from frost.models import (
    Idf,
    IdfAvailable,
    Lightning,
    Observations,
    ReportDut,
    ReportHumidityConstants,
    ReportIdf,
    ReportNormals,
    ReportStationRecords,
    ReportTemperatureConstants,
    ReportWindrose,
    ReportsAvailable,
)
from frost.utils.arrays import array_to_param

load_dotenv()


class APIError(Exception):
    """Raised when the API responds with a 400 or 404"""

    code: Optional[str]
    message: Optional[str]
    reason: Optional[str]

    def __init__(self, e) -> None:
        self.code = e.get("code")
        self.message = e.get("message")
        self.reason = e.get("reason")


class Frost(object):
    """Interface to frost.met.no API

    The Frost API key should be exposed as a environment variable called

    `FROST_API_KEY`

    or passed as a username parameter when creating and instance of the class.

    >>>  frost = Frost(username="myapikey")
    """

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> None:
        """
        Initialize the Frost API client
        :param Optional[str] client_id:
        The client id for the Frost API. Defaults to None
        :param Optional[str] client_secret:
        The client secret for the Frost API. Defaults to None
        """
        self.base_url = "https://frost-beta.met.no"
        self.api_version = "v1"
        self.session = requests.Session()
        self.client_id = client_id or getenv("FROST_CLIENT_ID", None)
        self.client_secret = client_secret or getenv("FROST_CLIENT_SECRET", None)

        if self.client_id is None:
            raise ValueError(
                """
                You must provide a client_id parameter
                or set the FROST_CLIENT_ID environment variable to
                use the Frost class
                """
            )
        if self.client_secret is None:
            raise ValueError(
                """
                You must provide a client_secret parameter
                or set the FROST_CLIENT_SECRET environment variable to
                use the Frost class
                """
            )

        self.session.auth = (self.client_id, self.client_secret)

    def let_it_go(self) -> str:
        return """
        Let it go, let it go
        Can't hold it back anymore
        Let it go, let it go
        Turn away and slam the door
        I don't care what they're going to say
        Let the storm rage on
        The cold never bothered me anyway
        """

    def make_request(
        self,
        endpoint: str,
        parameters_dict: dict,
    ) -> Union[
        IdfResponse,
        ObservationsResponse,
        LightningResponse,
        IdfAvailableResponse,
        ReportIdfResponse,
        ReportWindroseResponse,
        None,
    ]:
        """Make a request to the Frost API

        :param str endpoint: the endpoint to make the request to
        :param Any kwargs: the parameters to pass to the endpoint
        :raises APIError: APIError if the request fails
        :return Any: the response from the API
        """
        url = urljoin(self.base_url, f"api/{self.api_version}/{endpoint}/get?")

        # Make the request with the validated and structured parameters
        try:
            response = self.session.get(url, params=parameters_dict, timeout=60)
            response.raise_for_status()

            # If we got the status code for success
            if response.status_code == 200:
                json = response.json()

                ## If we got a data type status code (request succeeded)
                if "data" in json:
                    return json["data"]

                if "error" in json:
                    raise APIError(json["error"])
                else:
                    raise APIError(
                        {
                            "code": "no data",
                            "message": "no data field in json",
                        }
                    )

            # If we got an error type status code (request failed)
            else:
                raise APIError(
                    {
                        "code": "Arguments validation error",
                        "message": "\tstatus code: {}".format(response.status_code),
                    }
                )

        except requests.RequestException as e:
            # Handle exceptions related to the request
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": f"Request error: {str(e)}",
                }
            )

    def get_idf_available(
        self, sources: Optional[str | List[str]] = None
    ) -> IdfAvailable | None:
        """Get available IDF metadata (i.e. everything but the intensity values)
        for requested sources.

        :param Optional[str  |  List[str]] sources:
        The sources that you want available IDF metadata for. Enter a
        comma-separated list of words where each word is either an integer for a
        station ID or 'grid' for the gridded dataset.
        By default, metadata from all available sources are returned. Defaults to None
        :return IdfAvailable | None: IdfAvailable object
        """
        parameters = {}

        if sources != None:
            sources = array_to_param(sources)
            parameters["sources"] = sources

        try:
            # Validate the arguments
            params = IdfAvailableRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        parameters_dict = params.dict(exclude_unset=True, by_alias=True)

        data = self.make_request("idf/available", parameters_dict)

        if data == None:
            return None

        try:
            validated_data = IdfAvailableResponse.parse_obj(data)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        idf_available = IdfAvailable(validated_data)

        return idf_available

    def get_idf(
        self,
        sources: Optional[str | List[str]] = None,
        location: Optional[str] = None,
        durations: Optional[str | List[str]] = None,
        frequencies: Optional[str | List[str]] = None,
        unit: Optional[str] = None,
    ) -> Idf | None:
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

        if sources != None:
            parameters["sources"] = array_to_param(sources)

        if durations != None:
            parameters["durations"] = array_to_param(durations)

        if frequencies != None:
            parameters["frequencies"] = array_to_param(frequencies)

        if location != None:
            parameters["location"] = location

        if unit != None:
            parameters["unit"] = unit

        try:
            # Validate the arguments
            params = IdfRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        parameters_dict = params.dict(exclude_unset=True, by_alias=True)

        data = self.make_request("idf", parameters_dict)

        if data == None:
            return None

        try:
            validated_data = IdfResponse.parse_obj(data)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        idf = Idf(validated_data)

        return idf

    def get_lightning(
        self,
        reference_time: str = "latest",
        format: str = "json",
        geometry: Optional[str] = None,
    ) -> Lightning | None:
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

        try:
            # Validate the arguments
            params = LightningRequest(parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        parameters_dict = params.dict(exclude_unset=True, by_alias=True)

        data = self.make_request("lightning", parameters_dict)

        if data == None:
            return None

        try:
            validated_data = LightningResponse.parse_obj(data)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        lightning = Lightning(validated_data)
        return lightning

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

        :param bool include_observations: If you want to get weather observations set to True.
        If you only want information about the observations (metadata) set to
        False. Defaults to True
        :param str time: A time specification to select relevant observation times.
        Either a time range formated as "2020-01-01T00:00:00Z/2020-01-02T23:59:59Z",
        or the keyword latest can be used. By default if you use latest the
        maximum age of observations will be 3 hours, and only 1 latest observation will
        be returned. Defaults to "latest
        :param Optional[str  |  List[str]] element_ids: A comma-separated list of weather
        parameters. Use asterisk (*) for wildcard matching. Example: wind*,
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
        # Convert station_ids and element_ids to comma separated strings if they are lists

        parameters = {
            "station_ids": array_to_param(station_ids),
            "include_observations": include_observations,
            "time": time,
        }

        if location != None:
            parameters["location"] = time

        if element_ids != None:
            parameters["elementids"] = array_to_param(element_ids)

        if nearest != None:
            parameters["nearest"] = nearest

        if polygon != None:
            parameters["polygon"] = polygon

        try:
            # Validate the arguments
            params = ObservationsRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        parameters_dict = params.dict(exclude_unset=True, by_alias=True)

        # True or False to lowercase as the API expects it
        if "incobs" in parameters_dict:
            parameters_dict["incobs"] = str(parameters_dict["incobs"]).lower()

        data = self.make_request("obs/met.no/filter", parameters_dict)

        if data == None:
            return None

        validated_data = ObservationsResponse.parse_obj(data)

        observations = Observations(validated_data)

        return observations

    def get_report(
        self,
        type: str,
        settings: str,
    ) -> Union[
        ReportDutResponse,
        ReportHumidityConstantsResponse,
        ReportIdfResponse,
        ReportNormalsResponse,
        ReportStationRecordsResponse,
        ReportTemperatureConstantsResponse,
        ReportWindroseResponse,
        None,
    ]:
        """Get reports from the Frost API

        :param str type: type of report to get
        :param str settings:a stringifed json object containing
        the settings for the report
        :return Union[ IdfResponse, ObservationsResponse, LightningResponse,
        IdfAvailableResponse, ReportIdfResponse, ReportWindroseResponse,
        None, ]: Response from the API
        """
        parameters = {
            "type": type,
            "settings": settings,
        }

        try:
            # Validate the arguments
            report_request = ReportRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_request_dict = report_request.dict(exclude_unset=True, by_alias=True)

        data = self.make_request("reports", report_request_dict)

        if data == None:
            return None

        try:
            validated_data = ReportResponse.parse_obj(data)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        return validated_data

    def get_report_dut(self, source_id: str) -> ReportDut:
        """Get DUT reports from the Frost API

        :param str source_id: The source id to get the report for
        :return ReportDut: The DUT report
        """
        parameters = {
            source_id: source_id,
        }

        try:
            # Validate the arguments
            params = ReportDutRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("DUT", settings)

        try:
            data = ReportDutResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_dut = ReportDut(data)

        return report_dut

    def get_report_humidity_constants(
        self, source_id: str
    ) -> ReportHumidityConstants | None:
        """Get humidity constants reports from the Frost API

        :param str source_id: The source id to get the report for
        :return ReportIdf | None: The ReportHumidityConstants object or None
        """
        parameters = {
            source_id: source_id,
        }

        try:
            # Validate the arguments
            params = ReportHumidityConstantsRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("HumidityConstants", settings)

        try:
            data = ReportHumidityConstantsResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_humidity_constants = ReportHumidityConstants(data)

        return report_humidity_constants

    def get_report_idf(self, station_id: int, unit: str) -> ReportIdf | None:
        """Get IDF reports from the Frost API

        :param int station_id: The station id to get the report for
        :param str unit: The unit to get the report for. Available units are
        'mm', 'mm/h', 'mm/24h', 'mm/48h' or 'mm/72h'
        :return ReportIdf | None: The ReportIdf object or None
        """
        parameters = {
            station_id: station_id,
            unit: unit,
        }

        try:
            # Validate the arguments
            params = ReportIdfRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("IDF", settings)

        try:
            data = ReportIdfResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_idf = ReportIdf(data)

        return report_idf

    def get_report_normals(
        self, element_id: str, period: str, station_id: int
    ) -> ReportNormals | None:
        """_summary_

        :param str element_id: _description_
        :param str period: _description_
        :param int station_id: _description_
        :raises APIError: _description_
        :raises APIError: _description_
        :return ReportNormals | None: _description_
        """
        parameters = {
            element_id: element_id,
            period: period,
            station_id: station_id,
        }

        try:
            # Validate the arguments
            params = ReportNormalsRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("Normals", settings)

        try:
            data = ReportNormalsResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_normals = ReportNormals(data)

        return report_normals

    def get_report_station_records(
        self, station_id: int, record_category: str
    ) -> ReportStationRecords | None:

        parameters = {
            station_id: station_id,
            record_category: record_category,
        }

        try:
            # Validate the arguments
            params = ReportStationRecordsRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("StationRecords", settings)

        try:
            data = ReportStationRecordsResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_station_records = ReportStationRecords(data)

        return report_station_records

    def get_report_temperature_constants(
        self, station_id: int
    ) -> ReportTemperatureConstants | None:

        parameters = {
            station_id: station_id,
        }

        try:
            # Validate the arguments
            params = ReportTemperatureConstantsRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("TemperatureConstants", settings)

        try:
            data = ReportTemperatureConstantsResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        report_remperature_constants = ReportTemperatureConstants(data)

        return report_remperature_constants

    def get_report_windrose(
        self,
        station_id: int,
        from_time: str,
        to_time: str,
        max_wind_speed: Optional[int] = None,
        months: Optional[List[int]] = None,
        scale: Optional[ScaleType] = None,
    ) -> ReportWindrose | None:
        """Get windrose reports from the Frost API

        :param str settings: The serialized JSON object that contains the
        specification of a report of this type.
        :return Any: _description_
        """
        parameters: Dict[str, Union[str, int, List[int], ScaleType]] = {
            "station_id": station_id,
            "from_time": from_time,
            "to_time": to_time,
        }

        if max_wind_speed != None:
            parameters["Max_wind_speed"] = max_wind_speed

        if months != None:
            parameters["Months"] = months

        if scale != None:
            parameters["Scale"] = scale

        try:
            # Validate the arguments
            params = ReportWindroseRequest(**parameters)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        # Convert the validated parameters to a dictionary
        settings = params.json(exclude_unset=True, by_alias=True)

        report = self.get_report("windrose", settings)

        try:
            data = ReportWindroseResponse.parse_obj(report)
        except ValidationError as e:
            # Handle the validation error
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            )

        reportWindrose = ReportWindrose(data)

        return reportWindrose


def get_reports_available(self, type: Optional[str] = None) -> Any:
    """Get available reports from the Frost API

    :return Any: _description_
    """
    parameters = {
        "type": type,
    }

    try:
        # Validate the arguments
        params = ReportsAvailableRequest(**parameters)
    except ValidationError as e:
        # Handle the validation error
        raise APIError(
            {
                "code": "Arguments validation error",
                "message": e.json(),
            }
        )

    parameters_dict = params.dict(exclude_unset=True, by_alias=True)

    data = self.make_request("reports/available", parameters)

    if data == None:
        return None

    try:
        validated_data = ReportsAvailableResponse.parse_obj(data)
    except ValidationError as e:
        # Handle the validation error
        raise APIError(
            {
                "code": "Arguments validation error",
                "message": e.json(),
            }
        )

    reports_available = ReportsAvailable(validated_data)

    return reports_available
