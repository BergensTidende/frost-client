from __future__ import annotations

from typing import List

import pandas as pd

from frost.enteties import BaseEntity
from frost.models import ReportsAvailableResponse


class ReportsAvailable(BaseEntity[ReportsAvailableResponse]):
    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
        # tseries = self.data["tseries"]
        # if not tseries:
        #     return pd.DataFrame()

        # df = pd.DataFrame(tseries)

        # if df.empty:
        #     return df

        # df = df.reset_index()

        return pd.DataFrame()

    def to_list(self) -> List[str]:
        """Returns the sources as a Python list of dicts"""
        return [] if self.data is None else list(map(str, self.data))
