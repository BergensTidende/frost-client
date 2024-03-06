import json
import re
from typing import List, Optional

from frost.utils.arrays import param_to_array


def validate_nearest(v):
    try:
        nearest_data = json.loads(v)
        if not isinstance(nearest_data, dict):
            raise ValueError("Nearest must be a JSON object")

        # Validate the structure of 'nearest'
        required_keys = {"maxdist", "maxcount", "points"}
        if not required_keys.issubset(nearest_data):
            raise ValueError(
                f"Missing keys in nearest; required keys are: {required_keys}"
            )

        # Validate 'points'
        if not all(
            isinstance(point, dict) and "lon" in point and "lat" in point
            for point in nearest_data["points"]
        ):
            raise ValueError(
                "Each point in nearest must be a dictionary with 'lon' and 'lat' keys"
            )

    except json.JSONDecodeError:
        raise ValueError("Nearest must be valid JSON")

    return v


def validate_wkt(v: str):
    # Regular expression for matching basic WKT formats
    wkt_pattern = re.compile(
        r"^(POINT|LINESTRING|POLYGON|MULTIPOINT|MULTILINESTRING|MULTIPOLYGON|GEOMETRYCOLLECTION)\s*\(\s*(([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s*(,\s*[-+]?[0-9]*\.?[0-9]+\s+[-+]?[0-9]*\.?[0-9]+)*)\s*\)$",
        re.IGNORECASE,
    )
    return bool(wkt_pattern.match(v))


def validate_time(
    v: str, fieldname: str, allowed_keywords: Optional[str | List[str]] = None
):
    # Regular expression for the time format
    time_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"

    # Check if the input matches one of the allowed keywords
    if allowed_keywords != None:
        _allowed_keywords = param_to_array(allowed_keywords)

        if v in _allowed_keywords:
            return v

    # Check if the input matches the time pattern
    if not re.match(time_pattern, v):
        raise ValueError(
            f"{fieldname} must be in the format 'YYYY-MM-DDTHH:MM:SSZ'"
        )

    return v


def validate_time_range(
    v: str, fieldname: str, allowed_keywords: Optional[str | List[str]] = None
):
    # Regular expression for the time range format
    time_range_pattern = (
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    )

    # Check if the input matches the time range pattern
    if allowed_keywords != None:
        _allowed_keywords = param_to_array(allowed_keywords)

        if v not in _allowed_keywords and not re.match(time_range_pattern, v):
            raise ValueError(
                f"{fieldname} must be 'latest' or in the format 'YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ'"
            )
    else:
        if not re.match(time_range_pattern, v):
            raise ValueError(
                f"{fieldname} must be in the format 'YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ'"
            )
    return v
