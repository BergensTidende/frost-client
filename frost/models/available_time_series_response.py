from __future__ import annotations

from typing import List, Optional

import pandas as pd

from frost.models import Response, SourcesResponse
from frost.types import FrostObservationTimeSeriesResponse


class AvailableTimeSeriesResponse(Response):
    data: List[FrostObservationTimeSeriesResponse]

    def __init__(
        self,
        data: List[FrostObservationTimeSeriesResponse],
        sources: Optional[SourcesResponse] = None,
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourceResponse sources: Optional instance of sources response

        """
        self.data = data
        self.sources = sources
        self.date_columns = ["validFrom", "validTo"]
        self.compact_columns = [
            "stationId",
            "sourceId",
            "validFrom",
            "timeOffset",
            "timeResolution",
            "elementId",
            "unit",
        ]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :raises NotImplementedError: if not implemented in child class
        :return pd.DataFrame: the dataframe after normalization
        """
        return pd.json_normalize(self.data)

    def to_list(self) -> List[FrostObservationTimeSeriesResponse]:
        """Returns the sources as a Python list of dicts"""
        return self.data
