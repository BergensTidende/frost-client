from __future__ import annotations

from typing import List, Optional

import pandas as pd

from frost.models import Response, SourcesResponse
from frost.types import FrostRainfallIDFResponse


class FrequenciesResponse(Response):
    data: List[FrostRainfallIDFResponse]

    def __init__(
        self,
        data: List[FrostRainfallIDFResponse],
        sources: Optional[SourcesResponse] = None,
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourcesResponse sources: Optional instance of sources response

        """
        self.data = data
        self.sources = sources
        self.date_columns = ["validFrom", "validTo"]
        self.compact_columns = [
            "sourceId",
            "version",
            "validFrom",
            "validTo",
            "numberOfSeasons",
            "firstYearOfPeriod",
            "lastYearOfPeriod",
            "unit",
        ]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
        return pd.json_normalize(
            self.data,
        )

    def to_list(self) -> List[FrostRainfallIDFResponse]:
        """Returns the sources as a Python list of dicts"""
        return self.data
