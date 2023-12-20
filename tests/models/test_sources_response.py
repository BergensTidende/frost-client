import pandas as pd
import pytest
from frost.models.sources_response import SourcesResponse
from frost.types import FrostSource

# Test data
sources_data = [
    {
        "id": "1",
        "name": "Source1",
        "shortName": "S1",
        "county": "County1",
        "countyId": "C1",
        "municipality": "M1",
        "municipalityId": "M1",
    },
    {
        "id": "2",
        "name": "Source2",
        "shortName": "S2",
        "county": "County2",
        "countyId": "C2",
        "municipality": "M2",
        "municipalityId": "M2",
    },
]

# Test cases for parametrization
test_cases = [
    # Happy path
    {"input": sources_data, "expected": sources_data, "test_id": "happy_path"},
    # Edge case: empty list
    {"input": [], "expected": [], "test_id": "edge_empty_list"},
    # Error case: not a list
    {"input": "not a list", "expected": TypeError, "test_id": "error_not_a_list"},
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[tc["test_id"] for tc in test_cases]
)
def test_sources_response(test_case):
    # Arrange
    input_data = test_case["input"]
    expected = test_case["expected"]

    # Act
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            SourcesResponse(input_data)
    else:
        response = SourcesResponse(input_data)

        # Assert
        assert response.to_list() == expected
        assert response.to_ids_list() == [s["id"] for s in expected]
        assert response.normalize_json().equals(pd.json_normalize(expected))
