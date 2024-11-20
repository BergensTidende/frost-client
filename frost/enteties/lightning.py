from __future__ import annotations

from typing import List

import pandas as pd

from frost.api import ApiBase
from frost.models import LightningResponse, LightningRequest


class Lightning(ApiBase[LightningResponse]):
    date_columns = ["Epoch"]

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

    def to_list(self) -> List[str]:
        """Returns the sources as a Python list of dicts"""
        return self.data

    def get_ualf(self) -> str:
        """Returns data as text"""
        return self.data

    def get_lightning(
        self,
        reference_time: str = "latest",
        format: str = "json",
        geometry: Optional[str] = None,
    ) -> Lightning | None:
        """Get lightning data, very very frightening
        Get lightning data from the MET Norway's data storage systems. The query
        parameters act as a filter; if all were left blank (not allowed in practice),
        one would retrieve all of the lightning data in the system.
        Restrict the data using the query parameters.

        :param str referenceTime: The time range to get observations for in either
                                  extended ISO-8601 format or the single word 'latest'.
        :param str format: the return format. Either json or ualf, defaults to "json"
        :param Optional[str] geometry: Get lightning within a polygon specified as
        POLYGON(...) using WKT; Example: POLYGON((4 60, 4 59, 6 59, 6 60, 4 60)),
        defaults to None

        :return Any: A list of lightning data
        """
        parameters = {
            "reference_time": reference_time,
            "format": format,
            "geometry": geometry,
        }

        return self.validate_request_and_response(
            "lightning",
            LightningRequest,
            LightningResponse,
            Lightning,
            parameters,
        )
