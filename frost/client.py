from __future__ import annotations

from os import getenv
from typing import List, Optional, Union, cast
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from frost.models import (
    AvailableTimeSeriesResponse,
    FrequenciesResponse,
    FrequenciesSourcesResponse,
    ObservationsResponse,
    SourcesResponse,
)
from frost.types import (
    FrostAvailableSourcesFrequenciesArgs,
    FrostAvailableTimeSeriesArgs,
    FrostDataTypes,
    FrostFrequenciesArgs,
    FrostObservationsArgs,
    FrostObservationsResponse,
    FrostObservationTimeSeriesResponse,
    FrostRainfallIDFResponse,
    FrostResponse,
    FrostResponseError,
    FrostSourceArgs,
    FrostType,
)

load_dotenv()

class APIError(Exception):
    """Raised when the API responds with a 400 og 404"""

    code: str
    message: str
    reason: Optional[str]

    def __init__(self, e: FrostResponseError) -> None:
        self.code = e["code"] if "code" in e else None
        self.message = e["message"] if "message" in e else None
        self.reason = e["reason"] if "reason" in e else None


class Frost(object):

    """Interface to frost.met.no API

    The Frost API key should be exposed as a environment variable called

    `FROST_API_KEY`

    or passed as a username parameter when creating and instance of the class.

    >>>  frost = Frost(username="myapikey")
    """

    def __init__(
        self, username: Optional[str] = None
    ) -> None:
        """
        :param str username: your own frost.met.no username/key.
        """
        self.base_url = "https://frost.met.no/"
        self.api_version = "v0"
        self.session = requests.Session()
        self.username = username or getenv("FROST_API_KEY", None)

        if self.username is None:
            raise ValueError(
                """
                You must provide a username parameter
                or set the FROST_API_KEY environment variable to
                use the Frost class
                """
            )
        self.session.auth = (self.username, "")

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
        method: str,
        args: Union[
            FrostSourceArgs,
            FrostObservationsArgs,
            FrostAvailableTimeSeriesArgs,
            FrostAvailableSourcesFrequenciesArgs,
            FrostFrequenciesArgs,
        ],
    ) -> Optional[List[FrostDataTypes]]:
        url = urljoin(self.base_url, f"{method}/{self.api_version}.jsonld")

        stringified_args = {
            key: ",".join(map(str, value)) if isinstance(value, list) else str(value)
            for key, value in args.items()
        }

        response = self.session.get(url, params=stringified_args, timeout=60)

        if response.status_code < 200 or response.status_code > 500:
            response.raise_for_status()

        json: FrostResponse = response.json()

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

    def get_source_ids(self, result: Optional[List[FrostDataTypes]]) -> List[str]:
        """Get source IDs from a list of Frost API data types

        :param list args: list of Frost API data types

        :returns: list of source IDs

        """
        source_ids: List[str] = []

        if not result:
            return []

        # Iterate over all items, checking the type based on the "tag"
        for item in result:
            if isinstance(item, dict) and "sourceId" in item:
                response_item = cast(
                    Union[
                        FrostObservationsResponse,
                        FrostRainfallIDFResponse,
                        FrostObservationTimeSeriesResponse,
                    ],
                    item,
                )
                source_ids.append(response_item["sourceId"].split(":")[0])

        return list(set(source_ids))

    def get_sources(self, **kwargs: FrostType) -> SourcesResponse:
        """Get metadata for the source entitites defined in the Frost API.
        Use the query parameters to filter the set of sources returned.

        :param str ids: The Frost API source ID(s) that you want metadata for.
            Enter a  list or Python list to select multiple sources.
        :param str types: The type of Frost API source that
            you want metadata for.
        :param str geometry: Get Frost API sources defined by a
            specified geometry.
            Geometries are specified as either nearest(POINT(...)) or
            POLYGON(...)
        :param str nearestmaxcount: The maximum number of sources returned when
            using nearest(POINT(...)) for geometry. The default value is 1.
        :param str validtime: If specified, only sources that have been,
            or still are, valid/applicable during some part of this interval
            may be included in the result. Specify date/date;, date/now,
            dategt or now, where dategt is of the form YYYY-MM-DD,
            e.g. 2017-03-06.
            The default is 'now', i.e. only currently valid/applicable
            sources are included.
        :param str name: If specified, only sources whose 'name' attribute
            matches this. Enter at list seperated with comma or Python list.
        :param str country: If specified, only sources whose 'country'
            or 'countryCode' attribute matches this
        :param str county: If specified, only sources whose 'county'
            or 'countyId' attribute matches this .
        :param str municipality: If specified, only sources whose
             'municipality' or 'municipalityId' attribute matches this
        :param str wmoid: If specified, only sources whose 'wmoId'
            attribute matches this
        :param str stationholder: If specified, only sources whose
            'stationHolders' attribute contains at least one name that
            matches this
        :param str externalids: If specified, only sources whose 'externalIds'
            attribute contains at least one name that matches this
        :param str fields: A list or Python list of the fields that should be
            present in the response.

        :returns: :meth:`SourcesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        :examples:

            >>> f = Frost()
            >>> f.get_sources(county='46')

        """
        args = cast(FrostSourceArgs, kwargs)
        res = self.make_request("sources", args)

        if res is None:
            raise APIError({"code": "no data", "message": "no data field in json"})

        filtered_res = [item for item in res if item["tag"] == "FrostSource"]

        if filtered_res:
            return SourcesResponse(data=filtered_res)
        else:
            raise APIError(
                {
                    "code": "invalid data",
                    "message": "No valid FrostSource items found",
                }
            )

    def get_available_timeseries(
        self, include_sourcemeta: bool = False, **kwargs: FrostType
    ) -> AvailableTimeSeriesResponse:
        """Find timeseries metadata by source and/or element

        :param bool include_sourcemeta: If True will return a tuple with time
            series and source meta.
        :param list/str sources: The ID(s) of the data sources to get time
            series for
        :param str referencetime: The time range to get time series for as
            extended ISO-8601 format.
        :param list/str elements: The elements to get time series for as a
            list of Element ids.
        :param list/str timeoffsets: The time offsets to get time series for
            as a list of
            ISO-8601 periods, e.g. 'PT6H,PT18H'. If left out,
            the output is not filtered on time offset.
        :param list/str timeresolutions: The time resolutions to get time @
            series for as a list of
            ISO-8601 periods, e.g. 'PT6H,PT18H'. If left out,
            the output is not filtered on time resolution.
        :param str timeseriesids: The internal time series IDs to get time @
            series for as a
            list of integers, e.g. '0,1'. If left out,
            the output is not filtered on internal time series ID.
        :param str performancecategories: The performance categories to get
            time series for as a
            list of letters, e.g. 'A,C'. If left out,
            the output is not filtered on performance category.
        :param str exposurecategories: The exposure categories to get time
            series for as a
            list of integers, e.g. '1,2'.
            If left out, the output is not filtered on exposure category.
        :param str levels: The sensor levels to get observations for as a
            list of
            numbers, e.g. '0.1,2,10,20'. If left out, the output is not
            filtered on sensor level.
        :param str levelTypes: The sensor level types to get records for as a
            list of search filters
        :param str levelUnits: The sensor level units to get records for as a
            list of search filters
        :param str fields: Fields to include in the output as a  list.
            If specified, only these fields are included in the output.
            If left out, all fields are included.

        :returns: :meth:`AvailableTimeSeriesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        """
        args = cast(FrostAvailableTimeSeriesArgs, kwargs)

        res = self.make_request(
            "observations/availableTimeSeries",
            args,
        )

        sources = None

        if include_sourcemeta:
            source_ids = self.get_source_ids(res)
            sources = self.get_sources(ids=source_ids)

        if res is None:
            raise APIError({"code": "no data", "message": "no data field in json"})

        filtered_res = [
            item for item in res if item["tag"] == "FrostObservationTimeSeriesResponse"
        ]
        if filtered_res:
            return AvailableTimeSeriesResponse(data=filtered_res, sources=sources)
        else:
            raise APIError(
                {
                    "code": "invalid data",
                    "message": "No valid FrostObservationTimeSeriesResponse items",
                }
            )

    def get_observations(
        self, include_sourcemeta: bool = False, **kwargs: FrostType
    ) -> ObservationsResponse:
        """Get observation data from the Frost API.

        :param bool include_sourcemeta: If True will return a tuple
            with time series and source meta.
        :param list/str sources: The ID(s) of the data sources to get
            observations for as a  list of Frost API station
            IDs, e.g. _SN18700_ for Blindern.
        :param str referencetime: The time range to get observations
            for in either
            extended ISO-8601 format or the single word 'latest'.
        :param list/str elements: The elements to get observations for as a
            list of names that follow the Frost API naming convention.
        :param str format: The output format of the result. (required)
        :param str maxage: The maximum observation age as an ISO-8601 period,
            like 'P1D'. Applicable only when referencetime=latest. In general,
            the lower the value of maxage, the shorter the request will take
            to complete. The default value is 'PT3H'.
        :param str limit: The maximum number of observation times to be
            returned for each source/element combination, counting from the
            most recent time. Applicable only when referencetime=latest.
            Specify either 'all' to get all available times, or a positive
            integer. The default value is 1.
        :param list/str timeoffsets: The time offsets to get observations
            for as a  list of ISO-8601 periods, e.g. 'PT6H,PT18H'.
            If left out, the output is not filtered on time offset.
        :param list/str timeresolutions: The time resolutions to
            get observations for as a  list of ISO-8601 periods, e.g.
            'PT6H,PT18H'. If left out, the output is not filtered on time
            resolution.
        :param str timeseriesids: The internal time series IDs to get
            observations for as a  list of integers, e.g. '0,1'.
            If left out, the output is not filtered on internal time series ID.
        :param str performancecategories: The performance categories to
            get observations for as a  list of letters, e.g. 'A,C'.
            Enter a  list to specify multiple performance categories.
            If left out, the output is not filtered on performance category.
        :param str exposurecategories: The exposure categories to
            get observations for as a  list of integers, e.g. '1,2'.
            If left out, the output is not filtered on exposure category.
        :param str levels: The sensor levels to get observations for as a
            list of numbers, e.g. '0.1,2,10,20'.
            If left out, the output is not filtered on sensor level.
        :param str fields: Fields to include in the output as a
            list. If specified, only these fields are included in the output.
            If left out, all fields are included.

        :returns: :meth:`ObservationsResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        """
        args = cast(FrostObservationsArgs, kwargs)
        res = self.make_request("observations", args)

        sources = None

        if include_sourcemeta:
            source_ids = self.get_source_ids(res)
            sources = self.get_sources(ids=source_ids)

        if res is None:
            raise APIError({"code": "no data", "message": "no data field in json"})

        filtered_res = [
            item for item in res if item["tag"] == "FrostObservationsResponse"
        ]
        if filtered_res:
            return ObservationsResponse(data=filtered_res, sources=sources)
        else:
            raise APIError(
                {
                    "code": "invalid data",
                    "message": "No valid FrostObservationsResponse items found",
                }
            )

    def get_available_sources_frequencies(
        self, **kwargs: FrostType
    ) -> FrequenciesSourcesResponse:
        """Get available sources for rainfall IDF data

        :param list/str sources: The ID(s) of the data sources to get
            observations for as a  list of Frost API station
            IDs, e.g. _SN18700_ for Blindern.
        :param str types: The type(s) of Frost API source that you want information for.
            Enter a comma-separated list to select multiple types.
        :param str fields: A comma-separated list of the fields that should be present
            in the response. The sourceId attribute will always be returned in the
            query result. Leaving this parameter empty returns all attributes;
            otherwise only those properties listed will be visible in the result set
            (in addition to the sourceId)

        :returns: :meth:`FrequenciesSourcesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.
        """
        args = cast(FrostAvailableSourcesFrequenciesArgs, kwargs)
        res = self.make_request("frequencies/rainfall/availableSources", args)

        if res is None:
            raise APIError({"code": "no data", "message": "no data field in json"})

        filtered_res = [item for item in res if item["tag"] == "FrostRainfallIDFSource"]
        if filtered_res:
            return FrequenciesSourcesResponse(data=filtered_res)
        else:
            raise APIError(
                {
                    "code": "invalid data",
                    "message": "No valid FrostSource items found",
                }
            )

    def get_frequencies(
        self, include_sourcemeta: bool = False, **kwargs: FrostType
    ) -> FrequenciesResponse:
        """Get observation data from the Frost API.

        :param bool include_sourcemeta: If True will return a tuple
            with time series and source meta.
        :param list/str sources: The ID(s) of the data sources to get
            observations for as a  list of Frost API station
            IDs, e.g. _SN18700_ for Blindern.
        :param str location: The geographic position from which to get IDF data in case
            of a gridded dataset. Format: POINT(<longitude degrees> <latitude degrees>).
            Data from the nearest grid point is returned.
        :param str durations: The Frost API IDF duration(s), in minutes, that you want
            IDF data for. Enter a comma-separated list to select multiple durations.
        :param str frequencies: The Frost API IDF frequencies (return periods), in
            years, that you want IDF data for. Enter a comma-separated list to select
            multiple frequencies.
        :param str unit: The unit of measure for the intensity. Specify 'mm' for
            millimetres per minute multiplied by the duration, or 'lsha' for
            litres per second per hectar. The default unit is 'lsha'
        :param str fields: A comma-separated list of the fields that should be present
            in the response. The sourceId and values attributes will always be returned
            in the query result. Leaving this parameter empty returns all attributes;
            otherwise only those properties listed will be visible in the result set
            (in addition to the sourceId and values);
            e.g.: unit,numberOfSeasons will show only sourceId, unit, numberOfSeasons,
            and values in the response.


        :returns: :meth:`FrequenciesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        """
        args = cast(FrostFrequenciesArgs, kwargs)
        res = self.make_request("frequencies/rainfall", args)

        sources = None

        if include_sourcemeta:
            source_ids = self.get_source_ids(res)
            sources = self.get_sources(ids=source_ids)

        if res is None:
            raise APIError({"code": "no data", "message": "no data field in json"})

        filtered_res = [
            item for item in res if item["tag"] == "FrostRainfallIDFResponse"
        ]
        if filtered_res:
            return FrequenciesResponse(data=filtered_res, sources=sources)
        else:
            raise APIError(
                {
                    "code": "invalid data",
                    "message": "No valid FrostRainfallIDFResponse items found",
                }
            )
