import pandas as pd
import pytest

from disruptions.features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    add_features,
    cause_group,
    day_of_week,
    hour_of_day,
    is_rush_hour,
    n_stations,
)


def make_df(start_times, station_codes=None, cause_groups=None):
    n = len(start_times)
    return pd.DataFrame(
        {
            "start_time": pd.to_datetime(start_times),
            "rdt_station_codes": station_codes or ["AMR"] * n,
            "cause_group": cause_groups or ["weather"] * n,
        }
    )


def test_hour_and_day_of_week():
    df = make_df(["2025-01-06 07:30:00"])  # a Monday
    assert hour_of_day(df)["hour_of_day"].tolist() == [7]
    assert day_of_week(df)["day_of_week"].tolist() == [0]


@pytest.mark.parametrize(
    ("start_time", "expected"),
    [
        ("2025-01-06 07:00:00", True),  # Monday, start of morning rush
        ("2025-01-10 17:59:00", True),  # Friday, end of evening rush
        ("2025-01-06 06:59:00", False),
        ("2025-01-06 09:00:00", False),
        ("2025-01-06 12:00:00", False),
        ("2025-01-06 18:00:00", False),
        ("2025-01-11 08:00:00", False),  # Saturday
    ],
)
def test_is_rush_hour(start_time, expected):
    assert is_rush_hour(make_df([start_time]))["is_rush_hour"].tolist() == [expected]


def test_n_stations():
    df = make_df(["2025-01-06 12:00:00"] * 2, station_codes=["DT, DTCP, SDM", "AMR"])
    assert n_stations(df)["n_stations"].tolist() == [3, 1]


def test_cause_group_fills_missing_with_unknown():
    df = make_df(["2025-01-06 12:00:00"] * 2, cause_groups=["accidents", None])
    assert cause_group(df)["cause_group"].tolist() == ["accidents", "unknown"]


def test_cause_group_on_sample_disruptions(disruptions):
    expected = pd.Series(["accidents", "unknown", "weather"], name="cause_group")
    pd.testing.assert_series_equal(cause_group(disruptions)["cause_group"], expected)


def test_add_features_adds_all_columns_without_changing_input():
    df = make_df(["2025-01-06 07:30:00"], cause_groups=[None])
    original = df.copy()

    out = add_features(df)

    assert set(NUMERIC_FEATURES + CATEGORICAL_FEATURES) <= set(out.columns)
    assert out.loc[0, "is_rush_hour"]
    assert out.loc[0, "cause_group"] == "unknown"
    pd.testing.assert_frame_equal(df, original)
