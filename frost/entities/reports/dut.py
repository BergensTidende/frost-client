from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportDutResponse


class ReportDut(BaseEntity[ReportDutResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a DataFrame."""
        if self.data is None or (not self.data.summer and not self.data.winter):
            return pd.DataFrame()

        # Flatten summer items
        summer_records = [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "reference_period": self.data.reference_period,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "season": "summer",
                **summer_item.dict(),
            }
            for summer_item in self.data.summer
        ]

        # Flatten winter items
        winter_records = [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "reference_period": self.data.reference_period,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "season": "winter",
                **winter_item.dict(),
            }
            for winter_item in self.data.winter
        ]

        # Combine summer and winter records
        records = summer_records + winter_records

        # Create DataFrame
        df = pd.DataFrame(records)
        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the DUT data as a list of dictionaries."""
        if self.data is None or (not self.data.summer and not self.data.winter):
            return []

        # Convert summer and winter items into dictionaries
        summer_records = [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "reference_period": self.data.reference_period,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "season": "summer",
                **summer_item.dict(),
            }
            for summer_item in self.data.summer
        ]

        winter_records = [
            {
                "sourceid": self.data.sourceid,
                "first_year_of_period": self.data.first_year_of_period,
                "last_year_of_period": self.data.last_year_of_period,
                "number_of_seasons": self.data.number_of_seasons,
                "reference_period": self.data.reference_period,
                "seed_parameter": self.data.seed_parameter,
                "unit": self.data.unit,
                "updated_at": self.data.updated_at,
                "season": "winter",
                **winter_item.dict(),
            }
            for winter_item in self.data.winter
        ]

        # Combine summer and winter records
        return summer_records + winter_records
