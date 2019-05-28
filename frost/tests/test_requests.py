import unittest

from pandas import DataFrame

from frost.client import APIError, Frost
from frost.models import (AvailableTimeSeriesResponse, ObservationsResponse,
                          SourcesResponse)


class TestFrostRequests(unittest.TestCase):

    def setUp(self):
        self.f = Frost()

    def test_make_request(self):
        res = self.f.make_request('sources', county='12')
        self.assertIsInstance(res, list)

    def test_get_sources(self):
        res = self.f.get_sources(county='12')
        res_str = res.to_str()
        df_res = res.to_df()
        ids = res.to_ids_list()
        self.assertIsInstance(res, SourcesResponse)
        self.assertIsInstance(res_str, str)
        self.assertIsInstance(df_res, DataFrame)
        self.assertIsInstance(ids, list)

    def test_get_available_timeseries(self):
        res = self.f.get_available_timeseries(sources=['SN50500', 'SN50540'])
        self.assertIsInstance(res, AvailableTimeSeriesResponse)
        res_str = res.to_str()
        self.assertIsInstance(res_str, str)
        df_res = res.to_df()
        self.assertIsInstance(df_res, DataFrame)

    def test_get_available_timeseries_sourceids(self):
        res = self.f.get_available_timeseries(sources=['SN50500', 'SN50540'])
        ids = res.get_source_ids()
        self.assertIsInstance(ids, list)

    def test_get_available_timeseries_with_sources(self):
        res = self.f.get_available_timeseries(
            sources=['SN50500', 'SN50540'], include_sourcemeta=True)
        df = res.to_df()
        self.assertIn('source.shortName', df.columns)

    def test_get_observations_month(self):
        res = self.f.get_observations(
            sources=['SN50500', 'SN50540'],
            elements=['sum(precipitation_amount P1M)',
                      'mean(air_temperature P1M)'],
            timeoffsets='PT6H',
            referencetime='2019-01-01/2020-09-28')
        self.assertIsInstance(res, ObservationsResponse)
        self.assertIsInstance(res.to_str(), str)
        self.assertIsInstance(res.to_df(), DataFrame)

    def test_get_observations_day(self):
        res = self.f.get_observations(
            sources=['SN50540'],
            elements=['sum(precipitation_amount P1D)'],
            timeoffsets='PT6H',
            referencetime='2018-01-01/2018-02-01')
        df = res.to_df()
        self.assertIsInstance(res.to_str(), str)
        self.assertEqual(len(df), 31)
        self.assertTrue('referenceTime' in df.columns)

    def test_get_observations_hours(self):
        res = self.f.get_observations(
            sources=['SN50540'],
            elements=['sum(precipitation_amount PT1H)'],
            referencetime='2018-01-01/2018-02-01')
        df = res.to_df()
        self.assertIsInstance(res.to_str(), str)
        self.assertEqual(len(df), 31*24)
        self.assertTrue('referenceTime' in df.columns)

    def test_get_observations_error_400(self):
        with self.assertRaisesRegex(APIError, '400'):
            res = self.f.get_observations(
                sources=['SN50540XX'],
                elements=['sum(precipitation_amount PT1H)'],
                referencetime='2018-01-01/2018-02-01')

    def test_get_observations_no_data(self):
        with self.assertRaises(APIError) as cm:
            res = self.f.get_observations(
                sources=['SN50540'],
                elements=['sum(precipitation_amount PT1H)'],
                # timeoffsets='PT6H',
                referencetime='1890-01-01/1890-02-01')
        the_exception = cm.exception
        self.assertIsInstance(the_exception, APIError)
        self.assertEqual(
            str(the_exception),
            "{'code': 412, 'message': '412', 'reason': 'No time series found for this combination of parameters, check /observations/availableTimeSeries for more information.'}")

    def tearDown(self):
        self.f.session.close()

if __name__ == '__main__':
    unittest.main()
