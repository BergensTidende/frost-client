from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportHumidityConstantsResponse


class ReportHumidityConstants(BaseEntity[ReportHumidityConstantsResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a DataFrame."""
        if self.data is None or not self.data.values:
            return pd.DataFrame()

        # Convert the `values` object into a dictionary
        values_dict = self.data.values.dict()

        # Add time range to the dictionary
        values_dict["from_time"] = self.data.from_time
        values_dict["to_time"] = self.data.to_time

        # Create a DataFrame from the dictionary
        df = pd.DataFrame([values_dict])
        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the humidity constants data as a list of dictionaries."""
        if self.data is None:
            return []

        # Convert the `values` object into a dictionary and add time range
        values_dict = self.data.values.dict()
        values_dict["from_time"] = self.data.from_time
        values_dict["to_time"] = self.data.to_time

        return [values_dict]
