import pprint
from typing import Any, Dict, List


class SourcesResponse(object):
    """Response object for source endpoint"""

    def __init__(self, sources_json: List[Dict[str, Any]]) -> None:
        self.sources = sources_json

    def to_str(self) -> str:
        """Returns the string representation of the data"""
        return pprint.pformat(self.sources)

    # Set to Any so code works even if pandas is not installed
    def to_df(self, compact: bool = False) -> Any:
        """
        Returns a Pandas DataFrame representation of the model

        :param bool compact: If True returns a compact version with fewer
            columns

        """
        try:
            import pandas as pd
        except ImportError:
            # dependency missing, issue a warning
            import warnings

            warnings.warn(
                """
                Pandas dependency not found, please install with
                pip install frost-client[pandas] to enable to_df() feature
                """
            )
            return None
        else:
            df = pd.json_normalize(self.sources)

            # change date columns to datetime
            date_columns = ["validFrom", "validTo"]

            for c in date_columns:
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c], errors="coerce")

            if compact:
                compact_columns = [
                    "id",
                    "name",
                    "shortName",
                    "county",
                    "countyId",
                    "municipality",
                    "municipalityId",
                ]

                return df[compact_columns]
            return df

    def to_list(self) -> List[Dict[str, Any]]:
        """Returns the sources as a Python list of dicts"""
        return self.sources

    def to_ids_list(self) -> List[str]:
        """Returns only station IDs as a Python list"""

        return [s["id"] for s in self.sources]
