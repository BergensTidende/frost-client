from __future__ import annotations

from typing import List

import pandas as pd

from frost.enteties import BaseEntity
from frost.models import ReportTemperatureConstantsResponse


class ReportTemperatureConstants(BaseEntity[ReportTemperatureConstantsResponse]):
    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
        if self.data is None or "tseries" not in self.data:
            return pd.DataFrame()
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
        if self.data is None:
            return []
        return self.data if isinstance(self.data, list) else []
