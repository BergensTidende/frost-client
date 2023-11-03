from typing import List

import pandas as pd

from frost.models import Response
from frost.types import FrostRainfallIDFSource


class FrequenciesSourcesResponse(Response):
    """Response object for sources for frequnecises endpoint"""

    data: List[FrostRainfallIDFSource]

    def __init__(self, data: List[FrostRainfallIDFSource]) -> None:
        self.data = data
        self.date_colums = ["validFrom", "validTo"]
        self.compact_columns = [
            "sourceId",
            "version",
            "validFrom",
            "validTo",
            "numberOfSeasons",
            "firstYearOfPeriod",
            "lastYearOfPeriod",
        ]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :raises NotImplementedError: if not implemented in child class
        :return pd.DataFrame: the dataframe after normalization
        """
        return pd.json_normalize(self.data)

    def to_list(self) -> List[FrostRainfallIDFSource]:
        """Returns the sources as a Python list of dicts"""
        return self.data
