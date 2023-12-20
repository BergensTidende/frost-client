import pytest
import pandas as pd
from frost.models.response import Response
from frost.types import FrostSource

# Test data for parametrization
test_data = [
    # Happy path tests
    {
        "id": "HP1",
        "data": [{"tag": "FrostSource", "id": "FS:1"}],
        "sources": None,
        "expected": ["FS"],
    },
    {"id": "HP2", "data": [{"sourceId": "FS:2"}], "sources": None, "expected": ["FS"]},
    # Edge case tests
    {"id": "EC1", "data": [], "sources": None, "expected": []},
    {
        "id": "EC2",
        "data": [{"tag": "Unknown", "id": "FS:3"}],
        "sources": None,
        "expected": [],
    },
    # Error case tests
    {"id": "ER1", "data": [{"tag": "FrostSource"}], "sources": None, "expected": []},
    {"id": "ER2", "data": [{"sourceId": ""}], "sources": None, "expected": []},
]


@pytest.mark.parametrize("test_case", test_data, ids=[tc["id"] for tc in test_data])
def test_get_source_ids(test_case):
    # Arrange
    response = Response(test_case["data"], test_case["sources"])

    # Act
    result = response.get_source_ids()

    # Assert
    assert result == test_case["expected"]


def test_to_str():
    # Arrange
    data = [{"id": "FS:1", "tag": "FrostSource"}]
    response = Response(data)

    # Act
    result = response.to_str()

    # Assert
    assert result == str(data)


def test_normalize_json():
    # Arrange
    response = Response([])

    # Act & Assert
    with pytest.raises(NotImplementedError):
        response.normalize_json()


def test_to_df():
    # Arrange
    response = Response([])

    # Act & Assert
    with pytest.raises(NotImplementedError):
        response.to_df()


def test_to_list():
    # Arrange
    data = [{"tag": "FrostSource", "id": "FS:1"}]
    response = Response(data)

    # Act
    result = response.to_list()

    # Assert
    assert result == data


def test_merge_with_sources():
    # Arrange
    data = [{"tag": "FrostSource", "id": "FS:1"}]
    df = pd.DataFrame(data)
    response = Response(data)

    # Act
    result = response.merge_with_sources(df, False)

    # Assert
    assert result.equals(df)
