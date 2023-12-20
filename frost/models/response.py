from __future__ import annotations

import pprint
from typing import (
    TYPE_CHECKING,
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

from frost.types import (
    FrostObservationsResponse,
    FrostObservationTimeSeriesResponse,
    FrostRainfallIDFResponse,
    FrostRainfallIDFSource,
    FrostSource,
)
from frost.utils.dataframes import convert_date_columns, create_station_id_column

ResponseTypes = TypeVar(
    "ResponseTypes",
    FrostObservationsResponse,
    FrostObservationTimeSeriesResponse,
    FrostRainfallIDFResponse,
    FrostRainfallIDFSource,
    FrostSource,
)

if TYPE_CHECKING:
    from frost.models import SourcesResponse


class Response(Generic[ResponseTypes]):
    RET_TYPE: ClassVar[Callable]
    data: List[ResponseTypes]
    sources: Optional["SourcesResponse"]
    date_columns: List[str]
    compact_columns: List[str]

    def __init__(
        self, data: List[ResponseTypes], sources: Optional["SourcesResponse"] = None
    ) -> None:
        self.data = data
        self.sources = sources or None

    def to_str(self) -> str:
        """Returns the string representation of the data"""
        return pprint.pformat(self.data)

    def merge_with_sources(  # type: ignore[no-any-unimported]
        self, df: pd.DataFrame, compact: bool
    ) -> pd.DataFrame:
        """Merges the dataframe with the sources dataframe

        :param pd.DataFrame df: the dataframe to be merged
        :param bool compact: should the dataframe be compacted
        :return pd.DataFrame: the merged dataframe
        """
        if self.sources is None:
            return df
        sources_df = self.sources.to_df(compact=compact)
        sources_df = sources_df.add_prefix("source.")
        df = df.merge(sources_df, how="left", left_on="stationId", right_on="source.id")

        return df

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
        df = create_station_id_column(df)

        if compact:
            df = df[self.compact_columns]

        df = self.merge_with_sources(df, compact)
        return df

    def get_source_ids(self) -> List[str]:
        """Returns only station IDs as a Python list"""
        if not self.data:
            return []

        source_ids: List[str] = []

        # Iterate over all items, checking the type based on the "tag"
        for item in self.data:
            if isinstance(item, dict):
                if item.get("tag") == "FrostSource" and "id" in item:
                    source_item = cast(FrostSource, item)
                    source_ids.append(source_item["id"].split(":")[0])
            elif "sourceId" in item and item["sourceId"]:
                response_item = cast(
                    Union[
                        FrostRainfallIDFSource,
                        FrostRainfallIDFResponse,
                        FrostObservationsResponse,
                        FrostObservationTimeSeriesResponse,
                    ],
                    item,
                )
                source_ids.append(response_item["sourceId"].split(":")[0])

        return list(set(source_ids))

    def to_list(self) -> List[ResponseTypes]:
        """Returns the data as a Python list of dicts"""
        return self.data
