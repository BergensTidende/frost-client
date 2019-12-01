import pprint

class AvailableTimeSeriesResponse(object):

    def __init__(self, series_json, sources=None):
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourceResponse sources: Optional instance of sources response

        """
        self.series = series_json
        self.sources = sources

    def to_str(self):
        """Returns the string representation of the data"""
        return pprint.pformat(self.series)

    def to_df(self, compact=False):
        """
        Returns a Pandas DataFrame representation of the model

        :param bool compact: If True returns a compact version with fewer
            columns
        :param bool include_sourcemeta: If True will join in metadata
            (name etc) about the sources fewer columns

        """
        try:
            import pandas as pd
            from pandas.io.json import json_normalize
        except ImportError:
            # dependency missing, issue a warning
            import warnings
            warnings.warn('Pandas dependency not found, please install with pip install frost-client[pandas] to enable to_df() feature')
            return None
        else:
            compact_columns = [
                "stationId", "sourceId", "validFrom", "timeOffset",
                "timeResolution", "elementId",
                "unit"]

            df = json_normalize(self.series)

            # change date columns to datetime
            date_columns = ['validFrom', 'validTo']

            for c in date_columns:
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c])

            # create an extra column with normalized sourceId
            df["stationId"] = df['sourceId'].apply(lambda x: x.split(':')[0])

            if compact:
                df = df[compact_columns]

            # if we have metadataon the sources, merge it in
            if self.sources:
                sources_df = self.sources.to_df(compact=compact)
                sources_df = sources_df.add_prefix('source.')
                df = df.merge(sources_df, how="left", left_on="stationId",
                            right_on="source.id")

            return df

    def to_list(self):
        """Returns the sources as a Python list of dicts"""
        return self.series

    def get_source_ids(self):
        """Returns unique source ids as a list"""
        return list(set([s["sourceId"].split(':')[0] for s in self.series]))

    def to_ids_list(self):
        """Returns only station IDs as a Python list"""

        return [s['uri'] for s in self.series]
