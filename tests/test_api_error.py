import pytest
from frost.client import APIError
from frost.types import FrostResponseError

# Test data for parametrized test
test_data = [
    # Happy path tests
    {
        "id": "HP1",
        "input": {"code": "400", "message": "Bad Request"},
        "expected": ("400", "Bad Request", None),
    },
    {
        "id": "HP2",
        "input": {"code": "404", "message": "Not Found", "reason": "Invalid URL"},
        "expected": ("404", "Not Found", "Invalid URL"),
    },
    # Edge case tests
    {"id": "EC1", "input": {"code": "", "message": ""}, "expected": ("", "", None)},
    {
        "id": "EC2",
        "input": {"code": "500", "message": "Internal Server Error", "reason": ""},
        "expected": ("500", "Internal Server Error", ""),
    },
    # Error case tests
    {"id": "ER1", "input": {}, "expected": (None, None, None)},
    {
        "id": "ER2",
        "input": {"code": "400", "message": "Bad Request", "reason": None},
        "expected": ("400", "Bad Request", None),
    },
]


@pytest.mark.parametrize("test_case", test_data, ids=[tc["id"] for tc in test_data])
def test_api_error(test_case):
    # Arrange
    input_data = test_case["input"]
    expected_code, expected_message, expected_reason = test_case["expected"]
    error = FrostResponseError(**input_data)

    # Act
    api_error = APIError(error)

    # Assert
    assert api_error.code == expected_code
    assert api_error.message == expected_message
    assert api_error.reason == expected_reason
