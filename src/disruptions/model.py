"""Predict whether a disruption lasts longer than 60 minutes.

Run with: python -m disruptions.model
"""

import logging

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from disruptions.data import load_disruptions
from disruptions.features import CATEGORICAL_FEATURES, NUMERIC_FEATURES, add_features

LONG_DISRUPTION_MINUTES = 60

logger = logging.getLogger(__name__)


def make_target(df: pd.DataFrame) -> pd.Series:
    return (df["duration_minutes"] > LONG_DISRUPTION_MINUTES).astype(int)


def chronological_split(
    df: pd.DataFrame, test_size: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Train on the earliest rows and test on the latest.

    A random split would put one incident logged on several lines on both sides.
    """
    ordered = df.sort_values("start_time")
    cut = int(len(ordered) * (1 - test_size))
    return ordered.iloc[:cut], ordered.iloc[cut:]


def build_pipeline() -> Pipeline:
    preprocess = ColumnTransformer(
        [
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        [("preprocess", preprocess), ("classifier", LogisticRegression(max_iter=1000))]
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    df = load_disruptions()
    labelled = df.dropna(subset=["end_time", "duration_minutes"])
    logger.info("Dropped %d rows without an end_time", len(df) - len(labelled))

    train, test = chronological_split(add_features(labelled))
    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    y_train, y_test = make_target(train), make_target(test)

    model = build_pipeline().fit(train[features], y_train)
    majority_class = y_train.mode()[0]
    baseline = accuracy_score(y_test, [majority_class] * len(y_test))
    accuracy = accuracy_score(y_test, model.predict(test[features]))

    test_start = test["start_time"].min()
    print(f"Train rows: {len(train)}, test rows: {len(test)} (test from {test_start:%Y-%m-%d})")
    print(f"Baseline accuracy (majority class): {baseline:.3f}")
    print(f"Test accuracy: {accuracy:.3f}")


if __name__ == "__main__":
    main()
