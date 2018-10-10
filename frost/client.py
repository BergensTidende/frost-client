import os
from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth
from .models import SourcesResponse
from .models import AvailableTimeSeriesResponse
from .models import ObservationsResponse

FROST_API_KEY = os.environ.get('FROST_API_KEY', None)


class APIError(Exception):
    """ Raised when the API responds with a 400 og 404 """

    def __init__(self, e):
        self.code = e['code']


class Frost(object):

    """Interface to frost.met.no API

    The Frost API key should be exposed as a environment variable called

    `FROST_API_KEY`

    or passed as a username parameter when creating and instance of the class.

    >>>  frost = Frost(username="myapikey")
    """

    def __init__(self, username=None):
        """
        :param str username: your own frost.met.no username/key.
        """
        self.base_url = 'https://frost.met.no/'
        self.api_version = 'v0'
        self.session = requests.Session()
        self.username = username or FROST_API_KEY
        if not self.username:
            raise Exception(
                """
                You must provide a username parameter
                or set the FROST_API_KEY environment variable to
                use the Frost class
                """)
        self.session.auth = (self.username, '')

    def let_it_go(self):
        return """
        Let it go, let it go
        Can't hold it back anymore
        Let it go, let it go
        Turn away and slam the door
        I don't care what they're going to say
        Let the storm rage on
        The cold never bothered me anyway
        """

    def stringify_kwargs(self, kwargs):
        for key, value in kwargs.items():
            if type(kwargs[key]) == list:
                kwargs[key] = ",".join(value)
        return kwargs

    def make_request(self, method, **kwargs):
        """
        Make an API request, with all kwargs passed through as URL params
        """
        url = urljoin(self.base_url, method + '/' +
                      self.api_version + '.jsonld')
        response = self.session.get(
            url,
            params=kwargs, timeout=60)
        if response.status_code < 200 or response.status_code > 500:
            response.raise_for_status()
        json = response.json()
        if 'data' in json:
            return json['data']
        if 'error' in json:
            raise APIError(json['error'])
        return json

    def get_sources(self, **kwargs):
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
            matches this
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
        :param str externalid: If specified, only sources whose 'externalIds'
            attribute contains at least one name that matches this
        :param str fields: A  list of the fields that should be
            present in the response.

        :returns: :meth:`SourcesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        :examples:

            >>> f = Frost()
            >>> f.get_sources(county='12')

        """

        kwargs = self.stringify_kwargs(kwargs)

        res = self.make_request('sources',
                                **kwargs
                                )
        return SourcesResponse(res)

    def get_available_timeseries(self, include_sourcemeta=False, **kwargs):
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
        :param str level_types: The sensor level types to get records for as a
            list of search filters
        :param str level_units: The sensor level units to get records for as a
            list of search filters
        :param str fields: Fields to include in the output as a  list.
            If specified, only these fields are included in the output.
            If left out, all fields are included.

        :returns: :meth:`AvailableTimeSeriesResponse`

        :raises APIError: raises exception if error in the returned data or
            not found.

        """

        kwargs = self.stringify_kwargs(kwargs)

        res = self.make_request('observations/availableTimeSeries',
                                **kwargs
                                )

        sources = None

        if include_sourcemeta:
            source_ids = list(set([s["sourceId"].split(':')[0] for s in res]))
            sources = self.get_sources(ids=source_ids)

        return AvailableTimeSeriesResponse(res, sources=sources)

    def get_observations(self, include_sourcemeta=False, **kwargs):
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

        kwargs = self.stringify_kwargs(kwargs)

        res = self.make_request('observations',
                                **kwargs
                                )

        sources = None

        if include_sourcemeta:
            source_ids = list(set([s["sourceId"].split(':')[0] for s in res]))
            sources = self.get_sources(ids=source_ids)

        return ObservationsResponse(res, sources=sources)
