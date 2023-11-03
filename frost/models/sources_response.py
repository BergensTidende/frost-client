from typing import List

import pandas as pd

from frost.models import Response
from frost.types import FrostSource


class SourcesResponse(Response):
    """Response object for source endpoint"""

    data: List[FrostSource]

    def __init__(self, data: List[FrostSource]) -> None:
        self.data = data
        self.date_colums = ["validFrom", "validTo"]
        self.compact_columns = [
            "id",
            "name",
            "shortName",
            "county",
            "countyId",
            "municipality",
            "municipalityId",
        ]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :raises NotImplementedError: if not implemented in child class
        :return pd.DataFrame: the dataframe after normalization
        """
        return pd.json_normalize(self.data)

    def to_list(self) -> List[FrostSource]:
        """Returns the sources as a Python list of dicts"""
        return self.data

    def to_ids_list(self) -> List[str]:
        """Returns only station IDs as a Python list"""
        return [s["id"] for s in self.data]
