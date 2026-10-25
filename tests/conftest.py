import pandas as pd
import pytest


@pytest.fixture
def disruptions():
    return pd.DataFrame(
        {
            "start_time": pd.to_datetime(
                ["2025-01-06 07:30:00", "2025-01-08 12:00:00", "2025-01-11 03:15:00"]
            ),
            "rdt_station_codes": ["DT, DTCP, SDM", "AMR", None],
            "cause_group": ["accidents", None, "weather"],
        }
    )
