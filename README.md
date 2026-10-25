# What your AI cannot see

Predict whether a Dutch train disruption lasts longer than 60 minutes.

The model is a logistic regression trained on the 2025 disruptions in
`data/raw/disruptions-2025.csv`. It uses the hour and day of the week a
disruption starts, whether it starts in rush hour, how many stations it
affects, and its cause group. It trains on the earliest 80% of disruptions,
tests on the latest 20%, and reports its accuracy next to a majority-class
baseline.

## Install

You need [uv](https://docs.astral.sh/uv/). It installs Python 3.11 or newer if
you don't have it yet.

```sh
uv sync
```

## Run

```sh
uv run python -m disruptions.model
```

This prints the number of train and test rows, the baseline accuracy and the
test accuracy.

## Test

```sh
uv run pytest
```

## Credits

Data: Rijden de Treinen (rijdendetreinen.nl), licensed CC BY 4.0.
