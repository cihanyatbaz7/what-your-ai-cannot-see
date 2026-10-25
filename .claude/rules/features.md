---
paths:
  - "src/disruptions/features.py"
  - "tests/test_features.py"
---
# Feature conventions (team decisions)

- New code logs with the project logger, the way data.py does. Never use print(). Existing prints are removed in a separate change.
- A new feature function takes a pandas Series and returns a new Series. It never takes or changes the whole DataFrame. Older functions are converted in a separate change.
- Every new feature gets a test in tests/test_features.py that uses the disruptions fixture from tests/conftest.py and pandas.testing.assert_series_equal. Do not rewrite existing tests.
