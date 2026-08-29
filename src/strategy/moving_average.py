import pandas as pd


def moving_average_crossover(
    df,
    short_window=20,
    long_window=50,
):
    """
    Generate a moving-average crossover trading strategy.

    Strategy:
        - BUY  when short MA > long MA
        - SELL when short MA < long MA

    Parameters:
        df: pandas DataFrame containing a 'close' column
        short_window: short moving-average period
        long_window: long moving-average period

    Returns:
        pandas.DataFrame with:
            short_ma
            long_ma
            signal
            position
            strategy_return
            cumulative_strategy_return
    """

    if "close" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'close' column."
        )

    if short_window >= long_window:
        raise ValueError(
            "short_window must be smaller than long_window."
        )

    result = df.copy()

    # --------------------------------------------------
    # Calculate moving averages
    # --------------------------------------------------

    result["short_ma"] = (
        result["close"]
        .rolling(window=short_window)
        .mean()
    )

    result["long_ma"] = (
        result["close"]
        .rolling(window=long_window)
        .mean()
    )

    # --------------------------------------------------
    # Generate trading signal
    # --------------------------------------------------

    result["signal"] = 0

    result.loc[
        result["short_ma"] > result["long_ma"],
        "signal",
    ] = 1

    result.loc[
        result["short_ma"] < result["long_ma"],
        "signal",
    ] = -1

    # --------------------------------------------------
    # Generate position
    # --------------------------------------------------

    # Shift signal by one period to avoid
    # look-ahead bias.
    result["position"] = result["signal"].shift(1)

    result["position"] = (
        result["position"]
        .fillna(0)
    )

    # --------------------------------------------------
    # Calculate strategy returns
    # --------------------------------------------------

    if "daily_return" not in result.columns:
        result["daily_return"] = (
            result["close"]
            .pct_change()
        )

    result["strategy_return"] = (
        result["position"]
        * result["daily_return"]
    )

    # --------------------------------------------------
    # Calculate cumulative returns
    # --------------------------------------------------

    result["cumulative_strategy_return"] = (
        1 + result["strategy_return"].fillna(0)
    ).cumprod() - 1

    return result