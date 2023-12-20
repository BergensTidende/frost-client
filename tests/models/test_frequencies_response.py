import pandas as pd
import pytest

from frost.models.frequencies_response import FrequenciesResponse


@pytest.fixture
def frequencies_response():
    data = [
        {
            "sourceId": "SN18700",
            "version": 1,
            "validFrom": "1958-01-01T00:00:00.000Z",
            "validTo": "2019-12-31T00:00:00.000Z",
            "numberOfSeasons": 4,
            "firstYearOfPeriod": 1958,
            "lastYearOfPeriod": 2019,
            "unit": "mm",
        },
        {
            "sourceId": "SN18700",
            "version": 2,
            "validFrom": "2020-01-01T00:00:00.000Z",
            "validTo": "2021-12-31T00:00:00.000Z",
            "numberOfSeasons": 4,
            "firstYearOfPeriod": 2020,
            "lastYearOfPeriod": 2021,
            "unit": "mm",
        },
    ]
    return FrequenciesResponse(data)


def test_normalize_json(frequencies_response):
    expected_df = pd.DataFrame(
        {
            "sourceId": ["SN18700", "SN18700"],
            "version": [1, 2],
            "validFrom": ["1958-01-01T00:00:00.000Z", "2020-01-01T00:00:00.000Z"],
            "validTo": ["2019-12-31T00:00:00.000Z", "2021-12-31T00:00:00.000Z"],
            "numberOfSeasons": [4, 4],
            "firstYearOfPeriod": [1958, 2020],
            "lastYearOfPeriod": [2019, 2021],
            "unit": ["mm", "mm"],
        }
    )
    pd.testing.assert_frame_equal(frequencies_response.normalize_json(), expected_df)


def test_to_list(frequencies_response):
    expected_list = [
        {
            "sourceId": "SN18700",
            "version": 1,
            "validFrom": "1958-01-01T00:00:00.000Z",
            "validTo": "2019-12-31T00:00:00.000Z",
            "numberOfSeasons": 4,
            "firstYearOfPeriod": 1958,
            "lastYearOfPeriod": 2019,
            "unit": "mm",
        },
        {
            "sourceId": "SN18700",
            "version": 2,
            "validFrom": "2020-01-01T00:00:00.000Z",
            "validTo": "2021-12-31T00:00:00.000Z",
            "numberOfSeasons": 4,
            "firstYearOfPeriod": 2020,
            "lastYearOfPeriod": 2021,
            "unit": "mm",
        },
    ]
    assert frequencies_response.to_list() == expected_list
