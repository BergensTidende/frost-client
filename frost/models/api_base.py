from __future__ import annotations

import pprint
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
    cast,
)

import pandas as pd

from frost.utils.dataframes import convert_date_columns, create_station_id_column


class ApiBase:
    data: Any
    date_columns: List[str]
    compact_columns: List[str]

    def __init__(self, data) -> None:
        self.data = data

    def to_str(self) -> str:
        """Returns the string representation of the data"""
        return pprint.pformat(self.data)

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :raises NotImplementedError: if not implemented in child class
        :return pd.DataFrame: the dataframe after normalization
        """
        raise NotImplementedError(
            "normalize_json method must be implemented in child classes"
        )

    def to_df(  # type: ignore[no-any-unimported]
        self, compact: bool = False
    ) -> pd.DataFrame:
        df = self.normalize_json()
        df = convert_date_columns(df, self.date_columns)
        # df = create_station_id_column(df)

        if compact:
            df = df[self.compact_columns]

        return df

    def get_source_ids(self) -> List[str]:
        """Returns only station IDs as a Python list"""
        if not self.data:
            return []

        source_ids: List[str] = []

        # Iterate over all items, checking the type based on the "tag"
        # for item in self.data:
        #     if isinstance(item, dict):
        #         if item.get("tag") == "FrostSource" and "id" in item:
        #             source_item = cast(FrostSource, item)
        #             source_ids.append(source_item["id"].split(":")[0])
        #     elif "sourceId" in item and item["sourceId"]:
        #         response_item = cast(
        #             Union[
        #                 FrostRainfallIDFSource,
        #                 FrostRainfallIDFResponse,
        #                 FrostObservationsResponse,
        #                 FrostObservationTimeSeriesResponse,
        #             ],
        #             item,
        #         )
        #         source_ids.append(response_item["sourceId"].split(":")[0])

        return list(set(source_ids))

    def to_list(self) -> List[Any]:
        """Returns the data as a Python list of dicts"""
        return self.data

    def to_csv(self, path: str, compact: bool = False) -> None:
        """Writes the data to a CSV file"""
        df = self.to_df(compact=compact)
        df.to_csv(path, index=False)
