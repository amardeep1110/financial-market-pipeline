import pandas as pd
import pytest

from src.processing.validator import validate_market_data


def test_valid_market_data():

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                ["2026-01-01"]
            ),
            "open": [100],
            "high": [110],
            "low": [90],
            "close": [105],
            "volume": [1000],
        }
    )

    assert validate_market_data(df) is True


def test_invalid_market_data():

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                ["2026-01-01"]
            ),
            "open": [100],
            "high": [90],
            "low": [80],
            "close": [95],
            "volume": [1000],
        }
    )

    with pytest.raises(ValueError):
        validate_market_data(df)