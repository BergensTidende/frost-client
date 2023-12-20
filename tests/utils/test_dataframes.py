import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from frost.utils.dataframes import convert_date_columns, create_station_id_column

# Test cases for pytest.mark.parametrize
test_cases = [
    # Test case ID: 1
    # Happy path test with realistic test values
    {
        "id": "HP1",
        "input_df": pd.DataFrame(
            {"referenceTime": ["2022-01-01", "2022-01-02"], "value": [1, 2]}
        ),
        "date_columns": None,
        "expected_df": pd.DataFrame(
            {
                "referenceTime": pd.to_datetime(["2022-01-01", "2022-01-02"]),
                "value": [1, 2],
            }
        ),
    },
    # Test case ID: 2
    # Happy path test with multiple date columns
    {
        "id": "HP2",
        "input_df": pd.DataFrame(
            {
                "date1": ["2022-01-01", "2022-01-02"],
                "date2": ["2022-02-01", "2022-02-02"],
                "value": [1, 2],
            }
        ),
        "date_columns": ["date1", "date2"],
        "expected_df": pd.DataFrame(
            {
                "date1": pd.to_datetime(["2022-01-01", "2022-01-02"]),
                "date2": pd.to_datetime(["2022-02-01", "2022-02-02"]),
                "value": [1, 2],
            }
        ),
    },
    # Test case ID: 3
    # Edge case with empty DataFrame
    {
        "id": "EC1",
        "input_df": pd.DataFrame(),
        "date_columns": None,
        "expected_df": pd.DataFrame(),
    },
    # Test case ID: 4
    # Edge case with DataFrame that does not contain the specified date column
    {
        "id": "EC2",
        "input_df": pd.DataFrame({"value": [1, 2]}),
        "date_columns": ["date"],
        "expected_df": pd.DataFrame({"value": [1, 2]}),
    },
    # Test case ID: 5
    # Error case with non-date values in the date column
    {
        "id": "ER1",
        "input_df": pd.DataFrame(
            {"referenceTime": ["not a date", "also not a date"], "value": [1, 2]}
        ),
        "date_columns": None,
        "expected_error": ValueError,
    },
]


@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_convert_date_columns(test_case):
    # Arrange
    input_df = test_case["input_df"].copy()
    date_columns = test_case.get("date_columns")
    expected_df = test_case.get("expected_df")
    expected_error = test_case.get("expected_error")

    # Act
    if expected_error is not None:
        with pytest.raises(expected_error):
            convert_date_columns(input_df, date_columns)
    else:
        result_df = convert_date_columns(input_df, date_columns)

        # Assert
        assert_frame_equal(result_df, expected_df)


def test_create_station_id_column():
    # create a sample dataframe
    df = pd.DataFrame({"sourceId": ["123:abc", "456:def", "789:ghi"]})

    # create stationId column
    df = create_station_id_column(df)

    # check if the new column is created correctly
    assert df["stationId"].tolist() == ["123", "456", "789"]
