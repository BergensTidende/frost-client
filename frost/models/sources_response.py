import pprint


class SourcesResponse(object):
    """ Response object for source endpoint """

    def __init__(self, sources_json):
        self.sources = sources_json

    def to_str(self):
        """Returns the string representation of the data"""
        return pprint.pformat(self.sources)

    def to_df(self, compact=False):
        """
        Returns a Pandas DataFrame representation of the model

        :param bool compact: If True returns a compact version with fewer
            columns

        """
        try:
            from pandas.io.json import json_normalize
            import pandas as pd
        except ImportError:
            # dependency missing, issue a warning
            import warnings
            warnings.warn('Pandas dependency not found, please install with pip install frost-client[pandas] to enable to_df() feature')
            return None
        else:
            compact_columns = ["id", "name",
                            "shortName", "county", "countyId",
                            "municipality", "municipalityId"]

            df = json_normalize(self.sources)

            # change date columns to datetime
            date_columns = ['validFrom', 'validTo']

            for c in date_columns:
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c], errors='coerce')

            if compact:
                return df[compact_columns]
            return df

    def to_list(self):
        """Returns the sources as a Python list of dicts"""
        return self.sources

    def to_ids_list(self):
        """Returns only station IDs as a Python list"""

        return [s['id'] for s in self.sources]
