from typing import List, Optional

import pandas as pd


def convert_date_columns(  # type: ignore[no-any-unimported]
    df: pd.DataFrame, date_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """The `convert_date_columns` function converts specified date
    columns in a DataFrame to datetime format.

    :param  pd.DataFrame df: The DataFrame to be processed.

    :returns: pd.DataFrame
        The processed DataFrame with the specified date columns converted to
        datetime format.
    """
    if date_columns is None:
        date_columns = ["referenceTime"]

    for c in date_columns:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])

            # Check if the datetime objects are tz-aware and convert or localize accordingly
            if df[c].dt.tz is None:
                # If tz-naive, localize to "Europe/Oslo"
                df[c] = df[c].dt.tz_localize("Europe/Oslo")
            else:
                # If already tz-aware, convert to "Europe/Oslo"
                df[c] = df[c].dt.tz_convert("Europe/Oslo")
    return df


def create_station_id_column(  # type: ignore[no-any-unimported]
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Creates a new column in a DataFrame with the station ID based on the source ID.

    :param pd.DataFrame df: the DataFrame to be processed.
    :return pd.DataFrame: the processed DataFrame with the new column.
    """
    df["stationId"] = df["sourceId"].str.split(":").str[0]
    return df


def safe_parse_date(date_str) -> pd.Timestamp | None:
    if date_str is None:
        return None
    try:
        # Try to convert normally first
        fixed_date = pd.to_datetime(date_str)
        # Check if the datetime objects are tz-aware and convert or localize accordingly
        if fixed_date.tz is None:
            # If tz-naive, localize to "Europe/Oslo"
            fixed_date = fixed_date.tz_localize("Europe/Oslo")
        else:
            # If already tz-aware, convert to "Europe/Oslo"
            fixed_date = fixed_date.tz_convert("Europe/Oslo")

        return fixed_date
    except Exception:
        # If out of bounds, replace with a high but valid timestamp or None

        fallback_date = pd.to_datetime(
            "2262-04-11", format="%Y-%m-%d"
        )  # or pd.NaT, or None
        if fallback_date.tz is None:
            # If tz-naive, localize to "Europe/Oslo"
            fallback_date = fallback_date.tz_localize("Europe/Oslo")
        else:
            # If already tz-aware, convert to "Europe/Oslo"
            fallback_date = fallback_date.tz_convert("Europe/Oslo")

        return fallback_date
