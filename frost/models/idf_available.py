from __future__ import annotations

from typing import Any, List

import pandas as pd

from frost.api import IdfAvailableResponse
from frost.models import ApiBase
from frost.utils.dataframes import safe_parse_date

# from frost.types import FrostObservationsResponse


class IdfAvailable(ApiBase):
    data: IdfAvailableResponse

    def __init__(
        self,
        data: IdfAvailableResponse,
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourceResponse sources: Optional instance of sources response

        """
        self.data = data
        self.date_columns = ["Epoch"]
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

        :return pd.DataFrame: the dataframe after normalization
        """
        tseries = self.data["tseries"]
        if not tseries:
            return pd.DataFrame()

        df = pd.DataFrame(tseries)

        if df.empty:
            return df

        df = df.reset_index()

        return df

    def to_list(self) -> List[Any]:
        """Returns the sources as a Python list of dicts"""
        return self.data

    def get_ualf(self) -> str:
        """Returns data as text"""
        return self.data
