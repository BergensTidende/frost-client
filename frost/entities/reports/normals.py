from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportNormalsResponse


class ReportNormals(BaseEntity[ReportNormalsResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a DataFrame."""
        if self.data is None or not self.data.normals:
            return pd.DataFrame()

        # Convert the list of Normals objects into a list of dictionaries
        records = [normal.dict() for normal in self.data.normals]

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(records)

        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the normals data as a list of dictionaries."""
        if self.data is None or not self.data.normals:
            return []

        # Convert each Normals object into a dictionary
        return [normal.dict() for normal in self.data.normals]
