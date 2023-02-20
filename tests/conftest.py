import pytest

from frost.client import Frost

@pytest.fixture(scope="class")
def frost():
    return Frost()
