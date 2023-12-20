import os
import unittest
import pytest
from unittest.mock import patch, Mock
from frost.client import Frost, APIError

from frost.models import (
    AvailableTimeSeriesResponse,
    FrequenciesResponse,
    FrequenciesSourcesResponse,
    ObservationsResponse,
    SourcesResponse,
)


class TestFrost(unittest.TestCase):
    def setUp(self):
        self.frost = Frost(username="myapikey")

    def test_let_it_go(self):
        expected_lyrics = """
        Let it go, let it go
        Can't hold it back anymore
        Let it go, let it go
        Turn away and slam the door
        I don't care what they're going to say
        Let the storm rage on
        The cold never bothered me anyway
        """
        self.assertEqual(self.frost.let_it_go(), expected_lyrics)

    @patch("frost.client.requests.Session.get")
    def test_make_request(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"sourceId": "SN18700"}]}
        mock_get.return_value = mock_response

        result = self.frost.make_request("sources", {"ids": "SN18700"})
        self.assertEqual(result, [{"sourceId": "SN18700"}])

    @patch.dict(os.environ, {"FROST_API_KEY": "myapikey"})
    def test_init_with_env_variable(self):
        frost = Frost()
        self.assertEqual(frost.username, "myapikey")

    def test_init_without_username(self, skip_env=True):
        with self.assertRaises(ValueError):
            frost = Frost()

    @patch.dict(os.environ, {"FROST_API_KEY": "myapikey"})
    def test_init_with_env_variable(self):
        frost = Frost()
        self.assertEqual(frost.username, "myapikey")

    @patch("frost.client.requests.Session.get")
    def test_make_request_with_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": {"code": "invalid_parameter", "message": "Invalid parameter"}
        }
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.make_request("sources", {"ids": "SN18700"})

    @patch("frost.client.requests.Session.get")
    def test_make_request_with_no_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.make_request("sources", {"ids": "SN18700"})

    def test_get_source_ids(self):
        result = [
            {"sourceId": "SN18700:0:0"},
            {"sourceId": "SN18700:0:1"},
            {"sourceId": "SN18700:0:2"},
        ]
        source_ids = self.frost.get_source_ids(result)
        self.assertEqual(source_ids, ["SN18700"])

    def test_get_source_ids_with_empty_result(self):
        result = []
        source_ids = self.frost.get_source_ids(result)
        self.assertEqual(source_ids, [])

    @patch("frost.client.requests.Session.get")
    def test_get_sources(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "SourceResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostSource",
                    "@type": "SensorSystem",
                    "id": "SN18700",
                    "name": "OSLO - BLINDERN",
                    "shortName": "Blindern",
                    "country": "Norway",
                    "countryCode": "NO",
                    "wmoId": "1492",
                    "geometry": {"@type": "Point", "coordinates": "59.9423, 10.72"},
                    "distance": "40.575391309",
                    "masl": "94",
                    "validFrom": "1974-05-29T00:00:00.000Z",
                    "validTo": "2006-09-01T00:00:00.000Z",
                    "county": "Oppland",
                    "countyId": "5",
                    "municipality": "Lillehammer",
                    "municipalityId": "501",
                    "stationHolders": '[ "MET.NO", "STATENS VEGVESEN" ]',
                    "externalIds": '[ "01466", "10.249.0.126", "1466", "ENKJ" ]',
                    "icaoCodes": '[ "ESNZ", "ESPC" ]',
                    "shipCodes": '[ "JWBR", "LMXQ" ]',
                    "wigosId": "0-578-0-18700",
                },
                {
                    "tag": "FrostSource",
                    "@type": "SensorSystem",
                    "id": "SN18704",
                    "name": "BORD4 - BERGEN",
                    "shortName": "bord4Bergen",
                    "country": "Norway",
                    "countryCode": "NO",
                    "wmoId": "4",
                    "geometry": {"@type": "Point", "coordinates": "4, 4"},
                    "distance": "40.575391309",
                    "masl": "94",
                    "validFrom": "1978-07-08T00:00:00.000Z",
                    "validTo": "2049-09-01T00:00:00.000Z",
                    "county": "Vestland",
                    "countyId": "46",
                    "municipality": "Bergen",
                    "municipalityId": "4601",
                    "stationHolders": '[ "BT.NO" ]',
                    "externalIds": '[ "01466", "10.249.0.126", "1466", "ENKJ" ]',
                    "icaoCodes": '[ "ESNZ", "ESPC" ]',
                    "shipCodes": '[ "JWBR", "LMXQ" ]',
                    "wigosId": "0-578-0-18700",
                },
            ],
        }
        mock_get.return_value = mock_response

        result = self.frost.get_sources(ids=["SN18700", "SN18704"])
        self.assertIsInstance(result, SourcesResponse)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0]["id"], "SN18700")
        self.assertEqual(result.data[0]["name"], "OSLO - BLINDERN")
        self.assertEqual(result.data[1]["id"], "SN18704")
        self.assertEqual(result.data[1]["name"], "BORD4 - BERGEN")

    @patch("frost.client.requests.Session.get")
    def test_get_sources_with_no_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_sources(ids=["SN18700", "SN18701"])

    @patch("frost.client.requests.Session.get")
    def test_get_sources_with_invalid_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"tag": "NotFrostSource", "sourceId": "SN18700", "name": "My Source"}
        ]
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_sources(ids=["SN18700", "SN18701"])

    @patch("frost.client.requests.Session.get")
    def test_get_available_timeseries(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "ObservationTimeSeriesResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostObservationTimeSeriesResponse",
                    "sourceId": "SN18700",
                    "geometry": {"@type": "Point", "coordinates": "59.9423, 10.72"},
                    "level": {
                        "levelType": "height_above_ground",
                        "unit": "m",
                        "value": "10",
                    },
                    "validFrom": "1974-05-29",
                    "validTo": "1977-05-16",
                    "timeOffset": "PT18H",
                    "timeResolution": "P1D",
                    "timeSeriesId": "0",
                    "elementId": "air_temperature",
                    "unit": "degC",
                    "codeTable": "beaufort_scale",
                    "performanceCategory": "A",
                    "exposureCategory": "1",
                    "status": "string",
                    "uri": "string",
                    "userGroupIds": [0],
                }
            ],
        }
        mock_get.return_value = mock_response

        result = self.frost.get_available_timeseries(
            ids=["SN18700"]
        )

        self.assertIsInstance(result, AvailableTimeSeriesResponse)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0]["sourceId"], "SN18700")
        self.assertEqual(result.data[0]["timeResolution"], "P1D")
        self.assertEqual(result.data[0]["codeTable"], "beaufort_scale")
        self.assertEqual(result.data[0]["level"]["unit"], "m")

    @patch("frost.client.requests.Session.get")
    def test_get_available_sources_frequencies(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "RainfallIDFResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostRainfallIDFSource",
                    "sourceId": "SN18700",
                    "version": "1",
                    "validFrom": '["1974-05-29T12:00:00Z"]',
                    "validTo": '["2016-09-08T12:00:00Z"]',
                    "numberOfSeasons": "42",
                    "firstYearOfPeriod": "1968",
                    "lastYearOfPeriod": "2017",
                }
            ],
        }
        mock_get.return_value = mock_response

        result = self.frost.get_available_sources_frequencies(sources=["SN18700"])
        self.assertIsInstance(result, FrequenciesSourcesResponse)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0]["sourceId"], "SN18700")
        self.assertEqual(result.data[0]["numberOfSeasons"], "42")

    @patch("frost.client.requests.Session.get")
    def test_get_available_sources_frequencies_with_no_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_available_sources_frequencies(sources=["SN18700"])

    @patch("frost.client.requests.Session.get")
    def test_get_available_sources_frequencies_with_invalid_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"sourceId": "SN18700", "tag": "FrostOtherSource"}
        ]
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_available_sources_frequencies(sources=["SN18700"])

    @patch("frost.client.requests.Session.get")
    def test_get_frequencies(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "RainfallIDFResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostRainfallIDFResponse",
                    "sourceId": "SN18700",
                    "version": "1",
                    "geometry": {"@type": "Point", "coordinates": "59.9423, 10.72"},
                    "masl": "179",
                    "operatingPeriods": '["1974-05-29T12:00:00Z/1977-09-03T06:00:00Z", "1982-06-01T12:00:00/2016-09-08T12:00:00Z"]',
                    "numberOfSeasons": "42",
                    "firstYearOfPeriod": "1968",
                    "lastYearOfPeriod": "2017",
                    "unit": "l/s*Ha",
                    "values": [{"intensity": 322.8, "duration": 2, "frequency": 5}],
                }
            ],
        }
        mock_get.return_value = mock_response

        result = self.frost.get_frequencies(include_sourcemeta=False)
        self.assertIsInstance(result, FrequenciesResponse)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0]["sourceId"], "SN18700")
        self.assertEqual(len(result.data[0]["values"]), 1)
        self.assertEqual(result.data[0]["values"][0]["duration"], 2)
        self.assertEqual(result.data[0]["values"][0]["frequency"], 5)
        self.assertEqual(result.data[0]["values"][0]["intensity"], 322.8)

    @patch("frost.client.requests.Session.get")
    def test_get_frequencies_with_sourcemeta(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "tag": "FrostRainfallIDFResponse",
                "sourceId": "SN18700",
                "values": [
                    {"duration": 5, "frequency": 2, "intensity": 0.1},
                    {"duration": 5, "frequency": 5, "intensity": 0.2},
                ],
            }
        ]
        mock_get.return_value = mock_response

        result = self.frost.get_frequencies(include_sourcemeta=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], FrequenciesResponse)
        self.assertIsInstance(result[1], list)
        self.assertEqual(len(result[0].data), 1)
        self.assertEqual(result[0].data[0]["sourceId"], "SN18700")
        self.assertEqual(len(result[0].data[0]["values"]), 2)
        self.assertEqual(result[0].data[0]["values"][0]["duration"], 5)
        self.assertEqual(result[0].data[0]["values"][0]["frequency"], 2)
        self.assertEqual(result[0].data[0]["values"][0]["intensity"], 0.1)
        self.assertEqual(result[0].data[0]["values"][1]["duration"], 5)
        self.assertEqual(result[0].data[0]["values"][1]["frequency"], 5)
        self.assertEqual(result[0].data[0]["values"][1]["intensity"], 0.2)
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1][0]["sourceId"], "SN18700")

    @patch("frost.client.requests.Session.get")
    def test_get_observations(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "ObservationResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostObservationsResponse",
                    "sourceId": "SN18700",
                    "geometry": {"@type": "Point", "coordinates": "59.9423, 10.72"},
                    "referenceTime": "2012-12-24T11:00:00Z",
                    "observations": [
                        {
                            "elementId": "air_temperature",
                            "value": "12.7",
                            "origValue": "12.6",
                            "unit": "degC",
                            "codeTable": "beaufort_scale",
                            "level": {
                                "levelType": "height_above_ground",
                                "unit": "m",
                                "value": "10",
                            },
                            "timeOffset": "PT6H",
                            "timeResolution": "PT6H",
                            "timeSeriesId": "0",
                            "performanceCategory": "A",
                            "exposureCategory": "1",
                            "qualityCode": "0",
                            "controlInfo": "0111000000100010",
                            "dataVersion": "3",
                        }
                    ],
                }
            ],
        }
        mock_get.return_value = mock_response

        result = self.frost.get_observations(
            sources=["SN18700"],
            referencetime="2012-12-24T11:00:00Z",
            elements=["air_temperature"],
            format="json",
        )
        self.assertIsInstance(result, ObservationsResponse)
        self.assertEqual(result.data[0]["sourceId"], "SN18700")
        self.assertEqual(len(result.data[0]["observations"]), 1)
        self.assertEqual(
            result.data[0]["observations"][0]["elementId"], "air_temperature"
        )
        self.assertEqual(result.data[0]["observations"][0]["value"], "12.7")
        self.assertEqual(result.data[0]["observations"][0]["unit"], "degC")
        self.assertEqual(result.data[0]["observations"][0]["timeOffset"], "PT6H")
        self.assertEqual(result.data[0]["observations"][0]["performanceCategory"], "A")
        self.assertEqual(result.data[0]["observations"][0]["exposureCategory"], "1")
        self.assertEqual(result.data[0]["observations"][0]["level"]["unit"], "m")
        self.assertEqual(result.data[0]["observations"][0]["timeResolution"], "PT6H")
        self.assertEqual(result.data[0]["observations"][0]["timeSeriesId"], "0")

    @patch("frost.client.requests.Session.get")
    def test_get_observations_with_include_sourcemeta(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@context": "https://frost.met.no/schema",
            "@type": "ObservationResponse",
            "apiVersion": "v0",
            "license": "https://creativecommons.org/licenses/by/3.0/no/",
            "createdAt": "2007-11-06T16:34:41.000Z",
            "queryTime": "0.025",
            "currentItemCount": 3456,
            "itemsPerPage": 1000,
            "offset": 2000,
            "totalItemCount": 1000,
            "nextLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=3000",
            "previousLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=1000",
            "currentLink": "https://frost.met.no/resource/v0.jsonld?param=example_param&offset=2000",
            "data": [
                {
                    "tag": "FrostObservationsResponse",
                    "sourceId": "SN18700",
                    "geometry": {"@type": "Point", "coordinates": "59.9423, 10.72"},
                    "referenceTime": "2012-12-24T11:00:00Z",
                    "observations": [
                        {
                            "elementId": "air_temperature",
                            "value": "12.7",
                            "origValue": "12.6",
                            "unit": "degC",
                            "codeTable": "beaufort_scale",
                            "level": {
                                "levelType": "height_above_ground",
                                "unit": "m",
                                "value": "10",
                            },
                            "timeOffset": "PT6H",
                            "timeResolution": "PT6H",
                            "timeSeriesId": "0",
                            "performanceCategory": "A",
                            "exposureCategory": "1",
                            "qualityCode": "0",
                            "controlInfo": "0111000000100010",
                            "dataVersion": "3",
                        }
                    ],
                }
            ],
        }

        mock_get.return_value = mock_response

        result = self.frost.get_observations(
            sources=["SN18700"],
            referencetime="2022-01-01T00:00:00Z",
            elements=["air_temperature"],
            format="json",
            include_sourcemeta=True,
        )
        self.assertIsInstance(result, ObservationsResponse)

        self.assertEqual(result.data[0]["sourceId"], "SN18700")
        self.assertEqual(result.data[0]["elementId"], "air_temperature")
        self.assertEqual(result.data[0]["value"], -1.0)
        self.assertEqual(result.data[0]["unit"], "celsius")
        self.assertEqual(result.data[0]["timeOffset"], "PT0H")
        self.assertEqual(result.data[0]["performanceCategory"], "A")
        self.assertEqual(result.data[0]["exposureCategory"], 1)
        self.assertEqual(result.data[0]["level"], 2)
        self.assertEqual(result.data[0]["timeResolution"], "PT1H")
        self.assertEqual(result.data[0]["timeSeriesId"], 0)
        self.assertIsInstance(result.sources, SourcesResponse)

    @patch("frost.client.requests.Session.get")
    def test_get_observations_with_invalid_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"tag": "InvalidResponse"}]
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_observations(
                sources=["SN18700"],
                referencetime="2022-01-01T00:00:00Z",
                elements=["air_temperature"],
                format="json",
            )

    @patch("frost.client.requests.Session.get")
    def test_get_observations_with_no_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        with self.assertRaises(APIError):
            self.frost.get_observations(
                sources=["SN18700"],
                referencetime="2022-01-01T00:00:00Z",
                elements=["air_temperature"],
                format="json",
            )
