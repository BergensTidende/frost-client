import pprint
from typing import Any, Dict, List

from frost.models.sources_response import SourcesResponse


class FrequenciesResponse(object):
    def __init__(
        self, series_json: List[Dict[str, Any]], sources: SourcesResponse = None
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourcesResponse sources: Optional instance of sources response

        """
        self.series = series_json
        self.sources = sources

    def to_str(self) -> str:
        """Returns the string representation of the data"""
        return pprint.pformat(self.series)
