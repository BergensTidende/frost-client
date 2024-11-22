from __future__ import annotations

import pprint
from typing import Any, Generic, List, Optional, TypeVar

import pandas as pd

from frost.utils.dataframes import convert_date_columns

T = TypeVar("T")


class BaseEntity(Generic[T]):
    data: Optional[T] = None
    date_columns: List[str] = []
    compact_columns: List[str] = []

    def __init__(self, data: T) -> None:
        self.data = data

    def to_str(self) -> str:
        """Returns the string representation of the data"""
        return pprint.pformat(self.data)

    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :raises NotImplementedError: if not implemented in child class
        :return pd.DataFrame: the dataframe after normalization
        """
        raise NotImplementedError(
            "normalize_json method must be implemented in child classes"
        )

    def to_df(self, compact: bool = False) -> pd.DataFrame:
        df = self.normalize_json()
        df = convert_date_columns(df, self.date_columns)

        if compact:
            df = df[self.compact_columns].copy()

        # Ensure df is a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Expected df to be a pandas DataFrame.")

        return df

    def get_source_ids(self) -> List[str]:
        """Returns only station IDs as a Python list"""
        if not self.data:
            return []

        source_ids: List[str] = []

        return list(set(source_ids))

    def to_list(self) -> List[Any]:
        """Returns the data as a Python list of dicts"""
        raise NotImplementedError("to_list method must be implemented in child classes")

    def to_csv(self, path: str, compact: bool = False) -> None:
        """Writes the data to a CSV file"""
        df = self.to_df(compact=compact)
        df.to_csv(path, index=False)
