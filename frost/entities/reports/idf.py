from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportIdfResponse


class ReportIdf(BaseEntity[ReportIdfResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a DataFrame."""
        if self.data is None or not self.data.values:
            return pd.DataFrame()

        # Convert values into a list of dictionaries
        values_records = [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "quality_class": self.data.quality_class,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "duration": value.duration,
                "frequency": value.frequency,
                "intensity": value.intensity,
                "lowerinterval": value.lowerinterval,
                "upperinterval": value.upperinterval,
            }
            for value in self.data.values
        ]

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(values_records)
        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the IDF data as a list of dictionaries."""
        if self.data is None or not self.data.values:
            return []

        # Convert values into a list of dictionaries
        return [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "quality_class": self.data.quality_class,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "duration": value.duration,
                "frequency": value.frequency,
                "intensity": value.intensity,
                "lowerinterval": value.lowerinterval,
                "upperinterval": value.upperinterval,
            }
            for value in self.data.values
        ]
