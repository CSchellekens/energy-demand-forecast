import pandas as pd
import pytest

from energy_demand_forecasting.sources.base import validate


def test_validate_rejects_naive_timestamps() -> None:
    df = pd.DataFrame({"x": [1, 2]}, index=pd.date_range("2024-01-01", periods=2, freq="h"))
    with pytest.raises(ValueError, match="UTC"):
        validate(df, "test")


def test_validate_rejects_duplicates() -> None:
    index = pd.DatetimeIndex(["2024-01-01", "2024-01-01"], tz="UTC")
    df = pd.DataFrame({"x": [1, 2]}, index=index)
    with pytest.raises(ValueError, match="dubbele"):
        validate(df, "test")
