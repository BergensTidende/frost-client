from __future__ import annotations

from typing import List

import pandas as pd

from frost.api import IdfResponse
from frost.models import ApiBase


class Idf(ApiBase[IdfResponse]):
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
