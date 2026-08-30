import pandas as pd


def moving_average_crossover(
    df,
    short_window=20,
    long_window=50,
):
    """
    Moving-average crossover trading strategy.

    BUY:
        Short MA crosses above Long MA.

    SELL:
        Short MA crosses below Long MA.

    The position is shifted by one period
    to prevent look-ahead bias.
    """

    if "close" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'close' column."
        )

    if short_window >= long_window:
        raise ValueError(
            "short_window must be smaller than long_window."
        )

    if short_window <= 0 or long_window <= 0:
        raise ValueError(
            "Moving-average windows must be positive."
        )

    result = df.copy()

    # --------------------------------------------------
    # Moving averages
    # --------------------------------------------------

    result["short_ma"] = (
        result["close"]
        .rolling(short_window)
        .mean()
    )

    result["long_ma"] = (
        result["close"]
        .rolling(long_window)
        .mean()
    )

    # --------------------------------------------------
    # Trading signal
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
    # Detect crossover events
    # --------------------------------------------------

    previous_signal = result["signal"].shift(1)

    result["buy_signal"] = (
        (result["signal"] == 1)
        & (previous_signal <= 0)
    )

    result["sell_signal"] = (
        (result["signal"] == -1)
        & (previous_signal >= 0)
    )

    # --------------------------------------------------
    # Position
    # --------------------------------------------------

    result["position"] = (
        result["signal"]
        .shift(1)
        .fillna(0)
    )

    # --------------------------------------------------
    # Daily returns
    # --------------------------------------------------

    if "daily_return" not in result.columns:

        result["daily_return"] = (
            result["close"]
            .pct_change()
        )

    # --------------------------------------------------
    # Strategy returns
    # --------------------------------------------------

    result["strategy_return"] = (
        result["position"]
        * result["daily_return"]
    )

    # --------------------------------------------------
    # Cumulative strategy returns
    # --------------------------------------------------

    result["cumulative_strategy_return"] = (
        1 + result["strategy_return"].fillna(0)
    ).cumprod() - 1

    return result