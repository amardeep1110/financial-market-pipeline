import pandas as pd

from src.transformation.transformer import (
    calculate_daily_returns,
)


def test_calculate_daily_returns():
    """
    Test that daily returns are calculated correctly.
    """

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2026-01-01",
                    "2026-01-02",
                    "2026-01-03",
                ]
            ),
            "close": [
                100.0,
                110.0,
                99.0,
            ],
        }
    )

    result = calculate_daily_returns(df)

    # First row has no previous price
    assert pd.isna(result.iloc[0]["daily_return"])

    # 100 -> 110 = 10%
    assert abs(
        result.iloc[1]["daily_return"] - 0.10
    ) < 1e-10

    # 110 -> 99 = -10%
    assert abs(
        result.iloc[2]["daily_return"] - (-0.10)
    ) < 1e-10