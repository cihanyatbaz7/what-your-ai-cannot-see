"""One small function per feature, plus add_features to add them all."""

import pandas as pd

RUSH_HOURS = {7, 8, 16, 17}
KNOWN_CAUSE_GROUPS = {
    "accidents",
    "engineering work",
    "external",
    "infrastructure",
    "logistical",
    "rolling stock",
    "staff",
    "unknown",
    "weather",
}
NUMERIC_FEATURES = ["hour_of_day", "day_of_week", "is_rush_hour", "n_stations"]
CATEGORICAL_FEATURES = ["cause_group"]


def hour_of_day(df: pd.DataFrame) -> pd.DataFrame:
    df["hour_of_day"] = df["start_time"].dt.hour
    return df


def day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    """0 is Monday, 6 is Sunday."""
    df["day_of_week"] = df["start_time"].dt.day_of_week
    return df


def is_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Weekdays from 07:00 to 08:59 and from 16:00 to 17:59."""
    start = df["start_time"].dt
    df["is_rush_hour"] = (start.day_of_week < 5) & start.hour.isin(RUSH_HOURS)
    return df


def n_stations(df: pd.DataFrame) -> pd.DataFrame:
    """Number of station codes in the comma-separated rdt_station_codes column."""
    df["n_stations"] = (
        df["rdt_station_codes"]
        .fillna("")
        .map(lambda codes: sum(1 for code in codes.split(",") if code.strip()))
    )
    return df


def cause_group(df: pd.DataFrame) -> pd.DataFrame:
    df["cause_group"] = df["cause_group"].fillna("unknown")
    unexpected = set(df["cause_group"]) - KNOWN_CAUSE_GROUPS
    if unexpected:
        print(f"Unexpected cause_group values: {sorted(unexpected)}")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with every feature column added; df itself is left unchanged."""
    out = df.copy()
    out = hour_of_day(out)
    out = day_of_week(out)
    out = is_rush_hour(out)
    out = n_stations(out)
    out = cause_group(out)
    return out
