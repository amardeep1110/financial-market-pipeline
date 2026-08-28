import pandas as pd

from src.processing.cleaner import clean_market_data


def test_clean_market_data():
    """
    Test that market data is cleaned correctly.
    """

    df = pd.DataFrame(
        {
            "datetime": [
                "2026-01-03",
                "2026-01-01",
                "invalid-date",
            ],
            "open": [
                "120",
                "100",
                "bad",
            ],
            "high": [
                "125",
                "105",
                "bad",
            ],
            "low": [
                "118",
                "98",
                "bad",
            ],
            "close": [
                "122",
                "103",
                "bad",
            ],
            "volume": [
                "1000",
                "2000",
                "bad",
            ],
        }
    )

    result = clean_market_data(df)

    # Invalid row should be removed
    assert len(result) == 2

    # Numeric columns should be numeric
    assert pd.api.types.is_numeric_dtype(result["close"])

    # Dates should be datetime
    assert pd.api.types.is_datetime64_any_dtype(
        result["datetime"]
    )

    # Data should be sorted by datetime
    assert (
        result.iloc[0]["datetime"]
        < result.iloc[1]["datetime"]
    )