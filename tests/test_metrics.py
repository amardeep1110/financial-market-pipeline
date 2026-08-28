import pandas as pd

from src.analytics.metrics import (
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


def test_max_drawdown():
    """
    Test maximum drawdown calculation.
    """

    df = pd.DataFrame(
        {
            "close": [
                100,
                120,
                90,
                110,
                80,
            ]
        }
    )

    result = calculate_max_drawdown(df)

    # Maximum drawdown:
    # 120 -> 80 = -33.33%
    expected = (80 - 120) / 120

    assert abs(result - expected) < 1e-10


def test_sharpe_ratio():
    """
    Test Sharpe ratio calculation.
    """

    df = pd.DataFrame(
        {
            "daily_return": [
                0.01,
                0.02,
                0.015,
                0.01,
                0.025,
            ]
        }
    )

    result = calculate_sharpe_ratio(df)

    expected_mean = df["daily_return"].mean()
    expected_std = df["daily_return"].std()

    expected = (
        expected_mean / expected_std
    ) * (252 ** 0.5)

    assert abs(result - expected) < 1e-10