from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportWindroseResponse


class ReportWindrose(BaseEntity[ReportWindroseResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe."""
        if not self.data:
            return pd.DataFrame()

        horizontal_titles = self.data.horizontal_axis.titles
        vertical_titles = self.data.vertical_axis.titles
        data = self.data.table

        df = pd.DataFrame(data, index=vertical_titles, columns=horizontal_titles)

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        df = df.rename(columns={"index": "WindSpeed"})

        return df

    def get_metadata(self) -> Dict:
        """Returns the metadata as a Python dictionary."""
        return {} if self.data is None else self.data.metadata.dict()

    def get_extras(self) -> List[dict]:
        """Returns the extras as a Python list of dicts."""
        if self.data is None:
            return []
        return [extra.dict() for extra in self.data.extras]

    def get_windspeeds(self) -> Dict[str, float]:
        """Returns the windspeeds as a Python dictionary."""
        if self.data is None:
            return {}
        return dict(zip(self.data.vertical_axis.titles, self.data.vertical_axis.sums))

    def get_winddirections(self) -> Dict[str, float]:
        """Returns the wind directions as a Python dictionary."""
        if self.data is None:
            return {}
        return dict(
            zip(self.data.horizontal_axis.titles, self.data.horizontal_axis.sums)
        )

    def draw_windrose(self) -> None:
        """Draws the windrose using the data."""
        pass  # Implementation can be added as needed.

    def to_list(self) -> List[dict]:
        """Returns the data as a Python list of dictionaries."""
        return [] if self.data is None else [self.data.dict()]
