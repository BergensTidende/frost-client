import unittest
from frost.models.available_time_series_response import AvailableTimeSeriesResponse, FrostObservationTimeSeriesResponse
from unittest.mock import Mock

import pandas as pd

class TestAvailableTimeSeriesResponse(unittest.TestCase):

    def test_normalize_json(self):
        mock_data = [
            FrostObservationTimeSeriesResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                elementId="mean(air_temperature P1D)",
                unit="degree Celsius",
                timeOffset="PT0H",
                timeResolution="P1D",
                validFrom="2021-01-01T00:00:00Z",
                validTo="2021-01-02T00:00:00Z",
            ),
            FrostObservationTimeSeriesResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                elementId="mean(air_temperature P1D)",
                unit="degree Celsius",
                timeOffset="PT0H",
                timeResolution="P1D",
                validFrom="2021-01-02T00:00:00Z",
                validTo="2021-01-03T00:00:00Z",
            ),
        ]
        response = AvailableTimeSeriesResponse(data=mock_data)
        expected_df = pd.DataFrame({
            "stationId": ["SN18700", "SN18700"],
            "sourceId": ["SN18700:0:0", "SN18700:0:0"],
            "elementId": ["mean(air_temperature P1D)", "mean(air_temperature P1D)"],
            "unit": ["degree Celsius", "degree Celsius"],
            "timeOffset": ["PT0H", "PT0H"],
            "timeResolution": ["P1D", "P1D"],
            "validFrom": ["2021-01-01T00:00:00Z", "2021-01-02T00:00:00Z"],
            "validTo": ["2021-01-02T00:00:00Z", "2021-01-03T00:00:00Z"],
        })
        pd.testing.assert_frame_equal(response.normalize_json(), expected_df)

    def test_to_list(self):
        mock_data = [
            FrostObservationTimeSeriesResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                elementId="mean(air_temperature P1D)",
                unit="degree Celsius",
                timeOffset="PT0H",
                timeResolution="P1D",
                validFrom="2021-01-01T00:00:00Z",
                validTo="2021-01-02T00:00:00Z",
            ),
            FrostObservationTimeSeriesResponse(
                stationId="SN18700",
                sourceId="SN18700:0:0",
                elementId="mean(air_temperature P1D)",
                unit="degree Celsius",
                timeOffset="PT0H",
                timeResolution="P1D",
                validFrom="2021-01-02T00:00:00Z",
                validTo="2021-01-03T00:00:00Z",
            ),
        ]
        response = AvailableTimeSeriesResponse(data=mock_data)
        self.assertEqual(response.to_list(), mock_data)
