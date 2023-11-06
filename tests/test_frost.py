import pytest

from pandas import DataFrame

from frost.client import APIError, Frost
from frost.models import (
    AvailableTimeSeriesResponse,
    ObservationsResponse,
    SourcesResponse,
)

from frost.types import FrostResponseError

# Test data for happy path, edge cases, and error cases
test_data = [
    # Happy path tests with various realistic test values
    {
        "id": "HP1",
        "input": {
            "code": "400",
            "message": "Bad Request",
            "reason": "Invalid parameters",
        },
        "expected": {
            "code": "400",
            "message": "Bad Request",
            "reason": "Invalid parameters",
        },
    },
    {
        "id": "HP2",
        "input": {
            "code": "404",
            "message": "Not Found",
            "reason": "Resource not found",
        },
        "expected": {
            "code": "404",
            "message": "Not Found",
            "reason": "Resource not found",
        },
    },
    # Edge cases
    {
        "id": "EC1",
        "input": {"code": "", "message": "", "reason": ""},
        "expected": {"code": "", "message": "", "reason": ""},
    },
    # Error cases
    {
        "id": "EC1",
        "input": {
            "code": "500",
            "message": "Internal Server Error",
            "reason": "Server error",
        },
        "expected": {
            "code": "500",
            "message": "Internal Server Error",
            "reason": "Server error",
        },
    },
]


@pytest.mark.parametrize("test_case", test_data, ids=[tc["id"] for tc in test_data])
def test_api_error_init(test_case):
    # Arrange
    input_data = FrostResponseError(**test_case["input"])

    # Act
    api_error = APIError(input_data)

    # Assert
    assert api_error.code == test_case["expected"]["code"]
    assert api_error.message == test_case["expected"]["message"]
    assert api_error.reason == test_case["expected"]["reason"]


class TestFrostRequests:
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
            assert (
                str(the_exception)
                == "{'code': 412, 'message': '412', 'reason': 'No time series found for this combination of parameters, check /observations/availableTimeSeries for more information.'}"
            )
