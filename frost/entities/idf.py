from typing import List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import IdfResponse


class Idf(BaseEntity[IdfResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe."""
        if self.data is None or not self.data.sources:
            return pd.DataFrame()

        # Flatten sources and nested values
        records = []
        for source in self.data.sources:
            source_data = source.dict()  # Convert Source object to dictionary
            spatial_extent = source_data.pop("spatialExtent")  # Flatten spatialExtent
            values = source_data.pop("values")  # Extract values list

            for value in values:
                record = {**source_data, **spatial_extent, **value}
                records.append(record)

        # Create DataFrame
        df = pd.DataFrame(records)

        if df.empty:
            return df

        df = df.reset_index(drop=True)
        return df

    def to_list(self) -> List[dict]:
        """Returns the data as a list of dictionaries."""
        if self.data is None or not self.data.sources:
            return []

        # Convert each Source object to a dictionary
        sources_list = []
        for source in self.data.sources:
            source_data = source.dict()
            spatial_extent = source_data.pop("spatialExtent")
            source_data["spatialExtent"] = spatial_extent  # Keep nested structure
            sources_list.append(source_data)

        return sources_list
