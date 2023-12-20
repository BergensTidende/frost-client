import unittest
from frost.models.frequencies_sources_response import FrequenciesSourcesResponse
from frost.types import FrostRainfallIDFSource


class TestFrequenciesSourcesResponse(unittest.TestCase):

    def test_normalize_json(self):
        data = [
            FrostRainfallIDFSource(
                sourceId="source1",
                version=1,
                validFrom="2022-01-01",
                validTo="2022-12-31",
                numberOfSeasons=4,
                firstYearOfPeriod=1981,
                lastYearOfPeriod=2010,
            ),
            FrostRainfallIDFSource(
                sourceId="source2",
                version=2,
                validFrom="2023-01-01",
                validTo="2023-12-31",
                numberOfSeasons=3,
                firstYearOfPeriod=1986,
                lastYearOfPeriod=2015,
            ),
        ]
        response = FrequenciesSourcesResponse(data)
        expected_df = (
            response.normalize_json()
            .sort_values(by=["sourceId", "version"])
            .reset_index(drop=True)
        )
        expected_columns = [
            "sourceId",
            "version",
            "validFrom",
            "validTo",
            "numberOfSeasons",
            "firstYearOfPeriod",
            "lastYearOfPeriod",
        ]
        self.assertListEqual(list(expected_df.columns), expected_columns)
        self.assertEqual(expected_df.iloc[0]["sourceId"], "source1")
        self.assertEqual(expected_df.iloc[0]["version"], 1)
        self.assertEqual(expected_df.iloc[0]["validFrom"], "2022-01-01")
        self.assertEqual(expected_df.iloc[0]["validTo"], "2022-12-31")
        self.assertEqual(expected_df.iloc[0]["numberOfSeasons"], 4)
        self.assertEqual(expected_df.iloc[0]["firstYearOfPeriod"], 1981)
        self.assertEqual(expected_df.iloc[0]["lastYearOfPeriod"], 2010)
        self.assertEqual(expected_df.iloc[1]["sourceId"], "source2")
        self.assertEqual(expected_df.iloc[1]["version"], 2)
        self.assertEqual(expected_df.iloc[1]["validFrom"], "2023-01-01")
        self.assertEqual(expected_df.iloc[1]["validTo"], "2023-12-31")
        self.assertEqual(expected_df.iloc[1]["numberOfSeasons"], 3)
        self.assertEqual(expected_df.iloc[1]["firstYearOfPeriod"], 1986)
        self.assertEqual(expected_df.iloc[1]["lastYearOfPeriod"], 2015)

    def test_to_list(self):
        data = [
            FrostRainfallIDFSource(
                sourceId="source1",
                version=1,
                validFrom="2022-01-01",
                validTo="2022-12-31",
                numberOfSeasons=4,
                firstYearOfPeriod=1981,
                lastYearOfPeriod=2010,
            ),
            FrostRainfallIDFSource(
                sourceId="source2",
                version=2,
                validFrom="2023-01-01",
                validTo="2023-12-31",
                numberOfSeasons=3,
                firstYearOfPeriod=1986,
                lastYearOfPeriod=2015,
            ),
        ]
        response = FrequenciesSourcesResponse(data)
        expected_list = [
            {
                "sourceId": "source1",
                "version": 1,
                "validFrom": "2022-01-01",
                "validTo": "2022-12-31",
                "numberOfSeasons": 4,
                "firstYearOfPeriod": 1981,
                "lastYearOfPeriod": 2010,
            },
            {
                "sourceId": "source2",
                "version": 2,
                "validFrom": "2023-01-01",
                "validTo": "2023-12-31",
                "numberOfSeasons": 3,
                "firstYearOfPeriod": 1986,
                "lastYearOfPeriod": 2015,
            },
        ]
        self.assertListEqual(response.to_list(), expected_list)
