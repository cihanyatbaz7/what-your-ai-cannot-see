"""Load the 2025 train disruptions dataset."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "disruptions-2025.csv"


def load_disruptions(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the CSV and parse start_time and end_time; an empty end_time becomes NaT."""
    df = pd.read_csv(
        path, parse_dates=["start_time", "end_time"], date_format="%Y-%m-%d %H:%M:%S"
    )
    logger.info("Loaded %d rows from %s", len(df), path)
    return df
