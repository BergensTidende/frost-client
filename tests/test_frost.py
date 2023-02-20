import pytest

from pandas import DataFrame

from frost.client import APIError, Frost
from frost.models import (
    AvailableTimeSeriesResponse,
    ObservationsResponse,
    SourcesResponse,
)

class TestFrostRequests():
    def test_make_request(self, frost):
        res = frost.make_request("sources", county="46")
        assert isinstance(res, list)

    def test_get_sources(self, frost):
        res = frost.get_sources(county="46")
        res_str = res.to_str()
        df_res = res.to_df()
        ids = res.to_ids_list()
        assert isinstance(res, SourcesResponse)
        assert isinstance(res_str, str)
        assert isinstance(df_res, DataFrame)
        assert isinstance(ids, list)

    def test_get_available_timeseries(self, frost):
        res = frost.get_available_timeseries(sources=["SN50500", "SN50540"])
        assert isinstance(res, AvailableTimeSeriesResponse)
        res_str = res.to_str()
        assert isinstance(res_str, str)
        df_res = res.to_df()
        assert isinstance(df_res, DataFrame)


    def test_get_available_timeseries_sourceids(self, frost):
        res = frost.get_available_timeseries(sources=["SN50500", "SN50540"])
        ids = res.get_source_ids()
        assert isinstance(ids, list)

    def test_get_available_timeseries_with_sources(self, frost):
        res = frost.get_available_timeseries(
            sources=["SN50500", "SN50540"], include_sourcemeta=True
        )
        df = res.to_df()
        assert "source.shortName" in df.columns

    def test_get_observations_month(self, frost):
        res = frost.get_observations(
            sources=["SN50500", "SN50540"],
            elements=["sum(precipitation_amount P1M)", "mean(air_temperature P1M)"],
            timeoffsets="PT6H",
            referencetime="2019-01-01/2020-09-28",
        )
        assert isinstance(res, ObservationsResponse)
        assert isinstance(res.to_str(), str)
        assert isinstance(res.to_df(), DataFrame)

    def test_get_observations_day(self, frost):
        res = frost.get_observations(
            sources=["SN50540"],
            elements=["sum(precipitation_amount P1D)"],
            timeoffsets="PT6H",
            referencetime="2018-01-01/2018-02-01",
        )
        df = res.to_df()
        assert isinstance(res.to_str(), str)
        assert len(df) == 31
        assert "referenceTime" in df.columns

    def test_get_observations_hours(self, frost):
        res = frost.get_observations(
            sources=["SN50540"],
            elements=["sum(precipitation_amount PT1H)"],
            referencetime="2018-01-01/2018-02-01",
        )
        df = res.to_df()
        assert isinstance(res.to_str(), str)
        assert len(df) == 31 * 24
        assert "referenceTime" in df.columns

    def test_get_observations_no_data(self, frost):
        with pytest.raises(APIError) as cm:
            frost.get_observations(
                sources=["SN50540"],
                elements=["sum(precipitation_amount PT1H)"],
                # timeoffsets='PT6H',
                referencetime="1890-01-01/1890-02-01",
            )
            the_exception = cm.exception
            assert isinstance(the_exception, APIError)
            assert str(the_exception) == "{'code': 412, 'message': '412', 'reason': 'No time series found for this combination of parameters, check /observations/availableTimeSeries for more information.'}"
