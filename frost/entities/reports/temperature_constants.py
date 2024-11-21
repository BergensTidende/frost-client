from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportTemperatureConstantsResponse


class ReportTemperatureConstants(BaseEntity[ReportTemperatureConstantsResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe."""
        if self.data is None or not self.data.values:
            return pd.DataFrame()

        # Convert the `values` object into a dictionary
        values_dict = self.data.values.dict()

        # Create a DataFrame with the values and reset the index
        df = pd.DataFrame([values_dict])
        df["FromTime"] = self.data.from_time
        df["ToTime"] = self.data.to_time

        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the temperature constants as a list of dictionaries."""
        if self.data is None:
            return []

        # Convert the `values` object into a dictionary
        return [
            {
                "from_time": self.data.from_time,
                "to_time": self.data.to_time,
                **self.data.values.dict(),
            }
        ]
