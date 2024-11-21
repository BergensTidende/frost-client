from __future__ import annotations

from typing import Dict, List

import pandas as pd

from frost.entities import BaseEntity
from frost.models import ReportStationRecordsResponse
from frost.models.reports.station_records import Item


class ReportStationRecords(BaseEntity[ReportStationRecordsResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """Normalizes the JSON data into a DataFrame."""
        if self.data is None or self.data.station_id is None:
            return pd.DataFrame()

        # Flatten the data structure: min/max records and their months
        records = []

        def process_items(items: List[Item], category: str, time_period: str) -> None:
            """Helper function to flatten Item objects."""
            for item in items:
                for instance in item.instances:
                    records.append(
                        {
                            "station_id": self.data.station_id if self.data else "",
                            "record_category": (
                                self.data.record_category if self.data else ""
                            ),
                            "time_period": time_period,
                            "category": category,
                            "order": item.order,
                            "record_from": item.record_from,
                            "record_to": item.record_to,
                            "value": item.value,
                            "label": instance.label,
                            "obs_time": instance.obsTime,
                            "time_series_id": instance.timeSeriesID,
                        }
                    )

        # Process all-time min/max records
        process_items(self.data.min.alltime, "min", "alltime")
        process_items(self.data.max.alltime, "max", "alltime")

        # Process monthly min/max records
        for month, min_items in self.data.min.months.dict().items():
            process_items(min_items, "min", month)
        for month, max_items in self.data.max.months.dict().items():
            process_items(max_items, "max", month)

        # Convert flattened data into a DataFrame
        df = pd.DataFrame(records)
        return df.reset_index(drop=True)

    def to_list(self) -> List[Dict]:
        """Returns the data as a list of dictionaries."""
        if self.data is None:
            return []

        # Convert min/max records into a list of dictionaries
        records_list = []

        def process_items_to_dict(
            items: List[Item], category: str, time_period: str
        ) -> None:
            """Helper function to create dictionaries from Item objects."""
            for item in items:
                records_list.append(
                    {
                        "station_id": self.data.station_id if self.data else "",
                        "record_category": (
                            self.data.record_category if self.data else ""
                        ),
                        "time_period": time_period,
                        "category": category,
                        "order": item.order,
                        "record_from": item.record_from,
                        "record_to": item.record_to,
                        "value": item.value,
                        "instances": [instance.dict() for instance in item.instances],
                    }
                )

        # Process all-time min/max records
        process_items_to_dict(self.data.min.alltime, "min", "alltime")
        process_items_to_dict(self.data.max.alltime, "max", "alltime")

        # Process monthly min/max records
        for month, min_items in self.data.min.months.dict().items():
            process_items_to_dict(min_items, "min", month)
        for month, max_items in self.data.max.months.dict().items():
            process_items_to_dict(max_items, "max", month)

        return records_list
