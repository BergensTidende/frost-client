from __future__ import annotations

from typing import List, Optional

import pandas as pd

from frost.api import ApiBase
from frost.models.observations_models import ObservationsResponse, ObservationsRequest
from frost.utils.dataframes import safe_parse_date
from frost.utils.arrays import array_to_param


class Observations(ApiBase[ObservationsResponse]):
    date_columns = ["referenceTime"]

    def normalize_json(self) -> pd.DataFrame:  # type: ignore[no-any-unimported]
        """Normalizes the JSON data into a dataframe. This method must be implemented
        in child classes because the JSON structure is different for each endpoint.

        :return pd.DataFrame: the dataframe after normalization
        """
        data = self.data.dict() if self.data else {}
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

    def to_list(self) -> List[str]:
        """Returns the sources as a Python list of dicts"""
        return self.data.dict()["tseries"] if self.data else []

    def create_station_locations(self) -> dict:
        station_locations = {}

        data = self.data.dict() if self.data else {}

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
        # Step 2: Define a function to find the correct location based on time
        # and stationid
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
        # Assuming df_observations is your DataFrame containing observations
        # including 'time' and 'stationid'
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])

        # Check if the datetime objects are tz-aware and convert or localize accordingly
        def apply_find_location(row):
            # Assuming 'station_locations' is accessible and contains location
            # data mapped by stationId
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


def get_observations(
    self,
    include_observations: bool = True,
    time: str = "latest",
    element_ids: Optional[str | List[str]] = None,
    location: Optional[str] = None,
    station_ids: Optional[str | List[str]] = None,
    nearest: Optional[str] = None,
    polygon: Optional[str] = None,
) -> Observations | None:
    """
    This form allows a dataset of time series type 'filter' to be
    downloaded from the Frost API

    To make a valid request, you must specify the when, where and what of the
    observation data you want: you must set the time parameter,
    an element type parameter and at least one station or (geo)location type
    parameter. Matching is case-insensitive, and you can use asterisks (*) for
    wildcard matching.

    :param bool include_observations: If you want to get weather observations set
    to True. If you only want information about the observations (metadata) set to
    False. Defaults to True
    :param str time: A time specification to select relevant observation times.
    Either a time range formated as "2020-01-01T00:00:00Z/2020-01-02T23:59:59Z",
    or the keyword latest can be used. By default if you use latest the
    maximum age of observations will be 3 hours, and only 1 latest observation will
    be returned. Defaults to "latest
    :param Optional[str  |  List[str]] element_ids: A comma-separated list of
    weather parameters. Use asterisk (*) for wildcard matching. Example: wind*,
    air_temperature. Defaults to None
    :param Optional[str] location: The country, county, municipality or place name
    of the weather observations. Use asterisk (*) for wildcard matching.
    Example: *stad,bergen, defaults to None
    :param Optional[str | List[str]] station_ids: A comma-separated list of internal
    MET Norway weather station ID numbers. Use asterisk (*) for wildcard matching.
    Example: 18700,55*, defaults to None
    :param Optional[str] nearest: A geographic search parameter to look for weather
    observations around a geographic point.
    Example: {"maxdist":7.5,"maxcount":3,"points":[{"lon":10.72,"lat":59.94}]},
    defaults to None
    :param Optional[str] polygon: A geographic search parameter to look for weather
    observations inside a geographic area (specifically a polygon).
    Example: [{"lat":59.93,"lon":10.05},{"lat":59.93,"lon":11},
    {"lat":60.25,"lon":10.77}], defaults to None
    :return Observations: Weather observations object
    """

    parameters = {
        "station_ids": array_to_param(station_ids),
        "include_observations": include_observations,
        "time": time,
    }

    if location is not None:
        parameters["location"] = time

    if element_ids is not None:
        parameters["elementids"] = array_to_param(element_ids)

    if nearest is not None:
        parameters["nearest"] = nearest

    if polygon is not None:
        parameters["polygon"] = polygon

    return self.validate_request_and_response(
        "obs/met.no/filter",
        ObservationsRequest,
        ObservationsResponse,
        Observations,
        parameters,
    )
