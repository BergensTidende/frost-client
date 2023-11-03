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
