from __future__ import annotations

from typing import Any, List

import pandas as pd

from frost.api import ReportWindroseResponse
from frost.models import ApiBase
from frost.utils.dataframes import safe_parse_date


class ReportWindrose(ApiBase):
    data: ReportWindroseResponse

    def __init__(
        self,
        data: ReportWindroseResponse,
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourceResponse sources: Optional instance of sources response

        """
        self.data = data
        self.date_columns = []
        self.compact_columns = []

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
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

    def get_metadata(self) -> dict:
        """Returns the metadata as a Python dictionary"""
        return self.data.metadata.dict()

    def get_extras(self) -> List[dict]:
        """Returns the extras as a Python list of dicts"""
        return self.data.extras

    def get_windspeeds(self) -> dict[str, float]:
        """Returns the windspeeds as a Python dictionary"""
        data = dict(zip(self.data.vertical_axis.titles, self.data.vertical_axis.sums))

        return data

    def get_winddirections(self) -> dict:
        """Returns the winddirections as a Python dictionary"""

        data = dict(
            zip(self.data.horizontal_axis.titles, self.data.horizontal_axis.sums)
        )

        return data

    def draw_windrose(self):
        """Draws the windrose using the data"""

    def to_list(self) -> List[Any]:
        """Returns the sources as a Python list of dicts"""
        return self.data
