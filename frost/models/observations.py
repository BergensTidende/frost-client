from __future__ import annotations

from typing import Any, List

import pandas as pd

from frost.api import ObservationsResponse
from frost.models import ApiBase
from frost.utils.dataframes import safe_parse_date

# from frost.types import FrostObservationsResponse


class Observations(ApiBase):
    data: ObservationsResponse

    def __init__(
        self,
        data: ObservationsResponse,
    ) -> None:
        """
        Initialize a response class

        :param list series_json: List of data elements
        :param SourceResponse sources: Optional instance of sources response

        """
        self.data = data
        self.date_columns = ["referenceTime"]
        self.compact_columns = [
            "stationId",
            "sourceId",
            "validFrom",
            "timeOffset",
            "timeResolution",
            "elementId",
            "unit",
        ]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
        data = self.data.dict()
        tseries = data.get("tseries", None)
        if not tseries:
            return pd.DataFrame()

        df = pd.json_normalize(
            tseries,
            "observations",
            meta=[
                ["header", "id", "level"],
                ["header", "id", "parameterid"],
                ["header", "id", "sensor"],
                ["header", "id", "stationid"],
                ["header", "extra", "element", "description"],
                ["header", "extra", "element", "id"],
                ["header", "extra", "element", "name"],
                ["header", "extra", "element", "unit"],
                ["header", "extra", "station", "shortname"],
                ["header", "extra", "station", "location"],
                ["header", "extra", "timeseries", "geometry", "level", "unit"],
                ["header", "extra", "timeseries", "geometry", "level", "value"],
                ["header", "extra", "timeseries", "quality", "exposure"],
                ["header", "extra", "timeseries", "quality", "performance"],
                ["header", "extra", "timeseries", "timeoffset"],
                ["header", "extra", "timeseries", "timeresolution"],
                ["header", "available", "from"],
            ],
            errors="ignore",
        )

        if df.empty:
            return df

        df = df.reset_index()

        df = df.rename(
            columns={
                "time": "referenceTime",
                "body.qualitycode": "qualityCode",
                "body.value": "value",
                "header.id.level": "level",
                "header.id.parameterid": "parameterId",
                "header.id.sensor": "sensor",
                "header.id.stationid": "stationId",
                "header.extra.element.description": "description",
                "header.extra.element.id": "elementId",
                "header.extra.element.name": "name",
                "header.extra.element.unit": "unit",
                "header.extra.station.shortname": "shortname",
                "header.extra.station.location": "location",
                "header.extra.timeseries.geometry.level.unit": "geometryUnit",
                "header.extra.timeseries.geometry.level.value": "geometryValue",
                "header.extra.timeseries.quality.exposure": "exposure",
                "header.extra.timeseries.quality.performance": "performance",
                "header.extra.timeseries.timeoffset": "timeOffset",
                "header.extra.timeseries.timeresolution": "timeResolution",
                "header.available.from": "availableFrom",
            }
        )

        df = self.add_location(df)

        return df

    def to_list(self) -> List[Any]:
        """Returns the sources as a Python list of dicts"""
        return self.data.dict()["tseries"]

    def create_station_locations(self) -> Any:
        station_locations = {}

        data = self.data.dict()

        for entry in data["tseries"]:
            station_id = entry["header"]["id"]["stationid"]
            locations = entry["header"]["extra"]["station"]["location"]
            print(locations)
            for loc in locations:
                if "from_" in loc:
                    loc["from_time"] = safe_parse_date(loc["from_"])
                if "to" in loc:
                    loc["to_time"] = safe_parse_date(loc["to"])
            station_locations[station_id] = locations

        return station_locations

    def add_location(self, df: pd.DataFrame) -> pd.DataFrame:
        """adds the correct location to the observations by comparing the observation
        time with the location time intervals

        :param pd.DataFrame df: the dataframe to enrich with location data
        :return pd.DataFrame: the enriched dataframe
        """

        # Util function to find matching location for each observation
        # Step 2: Define a function to find the correct location based on time and stationid
        def find_location_for_station(
            obs_time, station_id, station_locations
        ) -> dict | None:
            if obs_time.tzinfo is None:
                obs_time = obs_time.tz_localize("Europe/Oslo")
            elif str(obs_time.tzinfo) != "Europe/Oslo":
                obs_time = obs_time.tz_convert("Europe/Oslo")

            locations = station_locations.get(station_id, [])
            for loc in locations:
                # Handle None values by defining open-ended logic
                if loc["from_time"] <= obs_time <= loc["to_time"]:
                    value = loc["value"]
                    for key in [
                        "latitude",
                        "longitude",
                        "elevation_masl_hs",
                    ]:  # Assuming these are the keys returned by your function
                        if key not in value:
                            value[key] = None  # Initialize the columns to None

                    return value

            return {
                "latitude": None,
                "longitude": None,
                "elevation_masl_hs": None,
            }

        station_locations = self.create_station_locations()

        # Step 3: Process observations to enrich them with location data
        # Assuming df_observations is your DataFrame containing observations including 'time' and 'stationid'
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])

        # Check if the datetime objects are tz-aware and convert or localize accordingly
        def apply_find_location(row):
            # Assuming 'station_locations' is accessible and contains location data mapped by stationId
            location = find_location_for_station(
                row["referenceTime"], row["stationId"], station_locations
            )
            return (
                pd.Series(location)
                if location
                else pd.Series(
                    {"latitude": None, "longitude": None, "elevation_masl_hs": None}
                )
            )

        df[["latitude", "longitude", "elevation_masl_hs"]] = df.apply(
            apply_find_location, axis=1, result_type="expand"
        )

        return df
