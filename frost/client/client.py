from __future__ import annotations

from os import getenv
from typing import Dict, List, Optional, Type, TypeVar, Union
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel

from frost.api import (
    IdfAvailableRequest,
    IdfAvailableResponse,
    IdfRequest,
    IdfResponse,
    LightningRequest,
    LightningResponse,
    ObservationsRequest,
    ObservationsResponse,
    ReportDutRequest,
    ReportDutResponse,
    ReportHumidityConstantsRequest,
    ReportHumidityConstantsResponse,
    ReportIdfRequest,
    ReportIdfResponse,
    ReportNormalsRequest,
    ReportNormalsResponse,
    ReportRequest,
    ReportResponse,
    ReportsAvailableRequest,
    ReportsAvailableResponse,
    ReportStationRecordsRequest,
    ReportStationRecordsResponse,
    ReportTemperatureConstantsRequest,
    ReportTemperatureConstantsResponse,
    ReportWindroseRequest,
    ReportWindroseResponse,
    ScaleType,
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
    ReportsAvailable,
    ReportStationRecords,
    ReportTemperatureConstants,
    ReportWindrose,
)
from frost.utils.arrays import array_to_param

load_dotenv()

T = TypeVar("T", bound=BaseModel)

class Frost:
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

            if response.status_code != 200:
                raise APIError(
                    {
                        "code": "Arguments validation error",
                        "message": f"\tstatus code: {response.status_code}",
                    }
                )

            json = response.json()

            # If we got a data type status code (request succeeded)
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

        except requests.RequestException as e:
            # Handle exceptions related to the request
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": f"Request error: {str(e)}",
                }
            ) from e

    def validate_request_and_response(
        self,
        request_type: str,
        request_model: Type[BaseModel],
        response_model: Type[BaseModel],
        return_model: Type[BaseModel],
        request_data: dict,
        report_response_model: Optional[Type[BaseModel]] = None,
    ) -> Union[
        IdfAvailableResponse,
        IdfResponse,
        ObservationsResponse,
        LightningResponse,
        ReportResponse,
        None,
    ]:
        try:
            validated_request = request_model(**request_data)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            ) from e

        request_dict = validated_request.dict(exclude_unset=True, by_alias=True)

        response_data = self.make_request(request_type, request_dict)

        if response_data is None:
            return None

        validated_data = None

        try:
            validated_data = response_model(**response_data)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            ) from e

        if validated_data is None:
            return None

        if request_type == "reports":
            report_data = response_model.parse_obj(response_data)
        else:
            return return_model(validated_data)

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

        if sources is not None:
            sources = array_to_param(sources)
            parameters["sources"] = sources

        return self.validate_request_and_response(
            "idf/available",
            IdfAvailableRequest,
            IdfAvailableResponse,
            IdfAvailable,
            parameters,
        )

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

        return self.validate_request_and_response(
            "idf",
            IdfRequest,
            IdfResponse,
            Idf,
            parameters,
        )

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

        return self.validate_request_and_response(
            "lightning",
            LightningRequest,
            LightningResponse,
            Lightning,
            parameters,
        )


    def get_report(
        self,
        report_type: str,
        report_request_model: Type[BaseModel],
        report_response_model: Type[BaseModel],
        report_return_model: Type[BaseModel],
        report_parameters: dict,
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

        params = report_request_model(**report_parameters)
        settings = params.json(exclude_unset=True, by_alias=True)

        parameters = {
            "type": report_type,
            "settings": settings,
        }

        return self.validate_request_and_response(
            "reports",
            ReportRequest,
            ReportResponse,
            report_return_model,
            parameters,
        )

    def get_report_dut(self, source_id: str) -> ReportDut:
        """Get DUT reports from the Frost API

        :param str source_id: The source id to get the report for
        :return ReportDut: The DUT report
        """
        parameters = {
            source_id: source_id,
        }

        return self.get_report(
            "DUT", ReportDutRequest, ReportDutResponse, ReportDut, parameters
        )

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
            ) from e

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
            ) from e

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
            ) from e

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
            ) from e

        report_idf = ReportIdf(data)

        return report_idf

    def get_report_normals(
        self, element_id: str, period: str, station_id: int
    ) -> ReportNormals | None:
        """_summary_

        :param str element_id: What element to get the report for
        :param str period: period of the report
        :param int station_id: station id to get the report for
        :raises APIError: if the request fails
        :return ReportNormals | None: Normals report object
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
            ) from e

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
            ) from e

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
            ) from e

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
            ) from e

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
            ) from e

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
            ) from e

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

        return self.get_report(
            "WindRose",
            ReportWindroseRequest,
            ReportWindroseResponse,
            ReportWindrose,
            parameters,
        )

    def get_reports_available(
        self, type: Optional[str] = None
    ) -> ReportsAvailable | None:
        """Get available reports from the Frost API

        :return Any: _description_
        """
        parameters = {
            "type": type,
        }

        return self.validate_request_and_response(
            "reports/available",
            ReportsAvailableRequest,
            parameters,
            ReportsAvailableResponse,
            ReportsAvailable,
        )
