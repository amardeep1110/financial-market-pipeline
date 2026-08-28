import pandas as pd


def calculate_sharpe_ratio(df, risk_free_rate=0.0):
    """
    Calculate the annualized Sharpe ratio.
    """

    returns = df["daily_return"].dropna()

    if returns.empty:
        return None

    daily_risk_free_rate = risk_free_rate / 252

    excess_returns = returns - daily_risk_free_rate

    if excess_returns.std() == 0:
        return None

    sharpe_ratio = (
        excess_returns.mean()
        / excess_returns.std()
    ) * (252 ** 0.5)

    return sharpe_ratio


def calculate_max_drawdown(df):
    """
    Calculate maximum drawdown from closing prices.
    """

    prices = df["close"].dropna()

    if prices.empty:
        return None

    running_max = prices.cummax()

    drawdown = (prices - running_max) / running_max

    return drawdown.min()
