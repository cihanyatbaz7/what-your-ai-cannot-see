"""One small function per feature, plus add_features to add them all."""

import pandas as pd

RUSH_HOURS = {7, 8, 16, 17}
NUMERIC_FEATURES = ["hour_of_day", "day_of_week", "is_rush_hour", "n_stations"]
CATEGORICAL_FEATURES = ["cause_group"]


def hour_of_day(df: pd.DataFrame) -> pd.Series:
    return df["start_time"].dt.hour


def day_of_week(df: pd.DataFrame) -> pd.Series:
    """0 is Monday, 6 is Sunday."""
    return df["start_time"].dt.day_of_week


def is_rush_hour(df: pd.DataFrame) -> pd.Series:
    """Weekdays from 07:00 to 08:59 and from 16:00 to 17:59."""
    return (day_of_week(df) < 5) & hour_of_day(df).isin(RUSH_HOURS)


def n_stations(df: pd.DataFrame) -> pd.Series:
    """Number of station codes in the comma-separated rdt_station_codes column."""
    return (
        df["rdt_station_codes"]
        .fillna("")
        .map(lambda codes: sum(1 for code in codes.split(",") if code.strip()))
    )


def cause_group(df: pd.DataFrame) -> pd.Series:
    return df["cause_group"].fillna("unknown")


FEATURES = {
    "hour_of_day": hour_of_day,
    "day_of_week": day_of_week,
    "is_rush_hour": is_rush_hour,
    "n_stations": n_stations,
    "cause_group": cause_group,
}


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with every feature column added; df itself is left unchanged."""
    out = df.copy()
    for name, feature in FEATURES.items():
        out[name] = feature(df)
    return out
