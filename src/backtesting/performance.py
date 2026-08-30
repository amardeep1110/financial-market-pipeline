import pandas as pd


def calculate_buy_and_hold_return(df):
    """
    Calculate total return for a buy-and-hold strategy.

    Parameters:
        df: DataFrame containing a 'close' column.

    Returns:
        float: Total buy-and-hold return.
    """

    if "close" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'close' column."
        )

    if len(df) < 2:
        return 0.0

    first_price = df["close"].iloc[0]
    last_price = df["close"].iloc[-1]

    return (last_price / first_price) - 1


def calculate_strategy_return(df):
    """
    Calculate total compounded return of the strategy.

    Requires:
        strategy_return
    """

    if "strategy_return" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'strategy_return' column."
        )

    returns = df["strategy_return"].fillna(0)

    return (1 + returns).prod() - 1


def calculate_cagr(df):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Uses the strategy's cumulative return and
    the number of years represented by the data.
    """

    if "strategy_return" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'strategy_return' column."
        )

    if "datetime" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'datetime' column."
        )

    if len(df) < 2:
        return 0.0

    dates = pd.to_datetime(df["datetime"])

    years = (
        dates.iloc[-1] - dates.iloc[0]
    ).days / 365.25

    if years <= 0:
        return 0.0

    total_return = calculate_strategy_return(df)

    if 1 + total_return <= 0:
        return -1.0

    return (1 + total_return) ** (1 / years) - 1


def calculate_strategy_sharpe_ratio(
    df,
    risk_free_rate=0.0,
):
    """
    Calculate annualized Sharpe Ratio for the strategy.
    """

    if "strategy_return" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'strategy_return' column."
        )

    returns = (
        df["strategy_return"]
        .dropna()
    )

    if len(returns) < 2:
        return 0.0

    daily_risk_free_rate = (
        risk_free_rate / 252
    )

    excess_returns = (
        returns - daily_risk_free_rate
    )

    standard_deviation = (
        excess_returns.std()
    )

    if standard_deviation == 0:
        return 0.0

    return (
        excess_returns.mean()
        / standard_deviation
    ) * (252 ** 0.5)


def calculate_strategy_max_drawdown(df):
    """
    Calculate maximum drawdown of the strategy.
    """

    if "strategy_return" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'strategy_return' column."
        )

    returns = (
        df["strategy_return"]
        .fillna(0)
    )

    equity_curve = (
        1 + returns
    ).cumprod()

    running_peak = (
        equity_curve.cummax()
    )

    drawdown = (
        equity_curve / running_peak
    ) - 1

    return drawdown.min()


def calculate_win_rate(df):
    """
    Calculate percentage of profitable strategy periods.
    """

    if "strategy_return" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'strategy_return' column."
        )

    returns = (
        df["strategy_return"]
        .dropna()
    )

    if len(returns) == 0:
        return 0.0

    winning_periods = (
        returns > 0
    ).sum()

    return winning_periods / len(returns)


def calculate_number_of_trades(df):
    """
    Calculate the number of position changes.

    A trade occurs whenever the strategy changes
    from one position to another.
    """

    if "position" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'position' column."
        )

    position = (
        df["position"]
        .fillna(0)
    )

    changes = (
        position.diff()
        .fillna(0)
        != 0
    )

    return int(changes.sum())


def calculate_performance_summary(
    df,
    transaction_cost=0.0,
):
    """
    Generate a complete backtesting performance summary.

    Parameters:
        df:
            DataFrame containing strategy results.

        transaction_cost:
            Cost applied per trade.
            Example:
                0.001 = 0.1%

    Returns:
        dict containing key performance metrics.
    """

    strategy_return = calculate_strategy_return(df)

    buy_and_hold_return = (
        calculate_buy_and_hold_return(df)
    )

    outperformance = (
        strategy_return
        - buy_and_hold_return
    )

    cagr = calculate_cagr(df)

    sharpe_ratio = (
        calculate_strategy_sharpe_ratio(df)
    )

    max_drawdown = (
        calculate_strategy_max_drawdown(df)
    )

    win_rate = calculate_win_rate(df)

    number_of_trades = (
        calculate_number_of_trades(df)
    )

    # --------------------------------------------------
    # Transaction costs
    # --------------------------------------------------

    if transaction_cost > 0:
        cost_multiplier = (
            1 - transaction_cost
        ) ** number_of_trades

        strategy_return_after_costs = (
            (1 + strategy_return)
            * cost_multiplier
        ) - 1

    else:
        strategy_return_after_costs = (
            strategy_return
        )

    return {
        "strategy_return": strategy_return,
        "strategy_return_after_costs": (
            strategy_return_after_costs
        ),
        "buy_and_hold_return": (
            buy_and_hold_return
        ),
        "outperformance": outperformance,
        "cagr": cagr,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "number_of_trades": number_of_trades,
    }


def calculate_transaction_costs(
    df,
    transaction_cost=0.001,
):
    """
    Calculate the total transaction costs.

    Parameters:
        df: DataFrame containing a 'position' column.
        transaction_cost: Cost per position change.
            Default = 0.001 (0.10%).

    Returns:
        float: Total transaction cost.
    """

    if "position" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'position' column."
        )

    if transaction_cost < 0:
        raise ValueError(
            "transaction_cost cannot be negative."
        )

    position_changes = (
        df["position"]
        .fillna(0)
        .diff()
        .abs()
    )

    total_cost = (
        position_changes
        * transaction_cost
    ).sum()

    return float(total_cost)
