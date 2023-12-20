import unittest
from frost.models.observations_response import (
    ObservationsResponse,
    FrostObservationsResponse,
)
from frost.models.sources_response import SourcesResponse


class TestObservationsResponse(unittest.TestCase):
    def test_normalize_json(self):
        data = [
            FrostObservationsResponse(
                sourceId="SN18700:0:0",
                referenceTime="2021-08-01T00:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 12.3},
                    {"elementId": "wind_speed", "value": 4.5},
                ],
            ),
            FrostObservationsResponse(
                sourceId="SN18700:0:1",
                referenceTime="2021-08-01T01:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 11.8},
                    {"elementId": "wind_speed", "value": 3.9},
                ],
            ),
        ]
        response = ObservationsResponse(data=data)
        df = response.normalize_json()
        expected_columns = [
            "elementId",
            "value",
            "sourceId",
            "referenceTime",
        ]
        expected_data = [
            ["air_temperature", 12.3, "SN18700:0:0", "2021-08-01T00:00:00Z"],
            ["wind_speed", 4.5, "SN18700:0:0", "2021-08-01T00:00:00Z"],
            ["air_temperature", 11.8, "SN18700:0:1", "2021-08-01T01:00:00Z"],
            ["wind_speed", 3.9, "SN18700:0:1", "2021-08-01T01:00:00Z"],
        ]

        self.assertEqual(list(df.columns), expected_columns)

        actual_data = [list(row) for row in df.itertuples(index=False, name=None)]
        self.assertEqual(actual_data, expected_data)

    def test_to_list(self):
        data = [
            FrostObservationsResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                referenceTime="2021-08-01T00:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 12.3},
                    {"elementId": "wind_speed", "value": 4.5},
                ],
            ),
            FrostObservationsResponse(
                stationId="SN18700",
                sourceId="SN18700:0:1",
                referenceTime="2021-08-01T01:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 11.8},
                    {"elementId": "wind_speed", "value": 3.9},
                ],
            ),
        ]
        response = ObservationsResponse(data=data)
        self.assertEqual(response.to_list(), data)

    def test_init(self):
        data = [
            FrostObservationsResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                referenceTime="2021-08-01T00:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 12.3},
                    {"elementId": "wind_speed", "value": 4.5},
                ],
            ),
            FrostObservationsResponse(
                stationId="SN18700",
                sourceId="SN18700:0:1",
                referenceTime="2021-08-01T01:00:00Z",
                observations=[
                    {"elementId": "air_temperature", "value": 11.8},
                    {"elementId": "wind_speed", "value": 3.9},
                ],
            ),
        ]
        sources = SourcesResponse(data=[{"sourceId": "SN18700"}])
        response = ObservationsResponse(data=data, sources=sources)
        self.assertEqual(response.data, data)
        self.assertEqual(response.sources, sources)
        self.assertEqual(response.date_columns, ["referenceTime"])
        self.assertEqual(
            response.compact_columns,
            [
                "stationId",
                "sourceId",
                "validFrom",
                "timeOffset",
                "timeResolution",
                "elementId",
                "unit",
            ],
        )
