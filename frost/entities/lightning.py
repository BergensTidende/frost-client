from __future__ import annotations

from typing import List

import pandas as pd

from frost.entities.base_entity import BaseEntity
from frost.models import LightningResponse


class Lightning(BaseEntity[LightningResponse]):
    date_columns = ["Epoch"]

    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe."""
        if self.data is None or not self.data.root:
            return pd.DataFrame()

        # Convert the list of LightningItems into a DataFrame
        df = pd.DataFrame([item.dict() for item in self.data.root])

        if df.empty:
            return df

        df = df.reset_index(drop=True)
        return df

    def to_list(self) -> List[dict]:
        """Returns the data as a list of dictionaries."""
        if self.data is None or not self.data.root:
            return []

        # Convert each LightningItem into a dictionary
        return [item.dict() for item in self.data.root]

    def get_ualf(self) -> str:
        """Returns data as text, if applicable."""
        if isinstance(self.data, LightningResponse):
            # Convert each LightningItem to a dictionary, then to a formatted string
            return "\n".join([str(item.dict()) for item in self.data.root])
        return ""
