import pandas as pd


def calculate_daily_returns(df):
    """
    Calculate daily percentage returns from closing prices.
    """

    df = df.copy()

    df = df.sort_values("datetime")

    df["daily_return"] = df["close"].pct_change()

    return df


def calculate_moving_averages(df):
    """
    Calculate 20-day and 50-day moving averages.
    """

    df = df.copy()

    df["ma_20"] = df["close"].rolling(window=20).mean()
    df["ma_50"] = df["close"].rolling(window=50).mean()

    return df

def calculate_volatility(df, window=20):
    """
    Calculate rolling volatility from daily returns.
    """

    df = df.copy()

    df["volatility_20"] = (
        df["daily_return"]
        .rolling(window=window)
        .std()
    )

    return df