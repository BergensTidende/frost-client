from __future__ import annotations

from typing import List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import IdfAvailableResponse


class IdfAvailable(BaseEntity[IdfAvailableResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe."""
        if not self.data or not self.data.sources:
            return pd.DataFrame()

        # Convert the list of Source objects into a DataFrame
        df = pd.DataFrame([source.dict() for source in self.data.sources])

        if df.empty:
            return df

        # Extract and flatten nested spatialExtent fields
        spatial_extent_df = pd.json_normalize(df.pop("spatialExtent").to_list())
        df = pd.concat([df, spatial_extent_df], axis=1)

        df = df.reset_index(drop=True)
        return df

    def to_list(self) -> List[dict]:
        """Returns the sources as a list of dictionaries."""
        if not self.data or not self.data.sources:
            return []

        # Convert each Source object to a dictionary
        return [source.dict() for source in self.data.sources]
