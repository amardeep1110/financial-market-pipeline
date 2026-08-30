
import pandas as pd


def calculate_position_size(
    capital,
    price,
    allocation=1.0,
):
    """
    Calculate number of shares that can be purchased.

    Example:
        capital = 100000
        price = 200
        allocation = 0.5

        Allocated capital = 50000
        Shares = 250
    """

    if capital < 0:
        raise ValueError(
            "capital cannot be negative."
        )

    if price <= 0:
        raise ValueError(
            "price must be greater than zero."
        )

    if not 0 < allocation <= 1:
        raise ValueError(
            "allocation must be greater than 0 "
            "and less than or equal to 1."
        )

    allocated_capital = (
        capital * allocation
    )

    return int(
        allocated_capital / price
    )


def calculate_position_value(
    shares,
    price,
):
    """
    Calculate the market value of a position.
    """

    if shares < 0:
        raise ValueError(
            "shares cannot be negative."
        )

    if price < 0:
        raise ValueError(
            "price cannot be negative."
        )

    return float(
        shares * price
    )


def calculate_trade_profit_loss(
    entry_price,
    exit_price,
    shares,
):
    """
    Calculate profit or loss from a trade.
    """

    if entry_price <= 0:
        raise ValueError(
            "entry_price must be greater than zero."
        )

    if exit_price < 0:
        raise ValueError(
            "exit_price cannot be negative."
        )

    if shares < 0:
        raise ValueError(
            "shares cannot be negative."
        )

    return float(
        (exit_price - entry_price)
        * shares
    )

def calculate_portfolio_value(
    df,
    initial_capital=100000.0,
    allocation=1.0,
):
    """
    Calculate portfolio equity using strategy positions.

    The initial allocation is calculated using the
    first available closing price.

    Parameters:
        df:
            DataFrame containing 'close' and 'position'.

        initial_capital:
            Starting portfolio capital.

        allocation:
            Percentage of capital allocated to a trade.

    Returns:
        DataFrame containing:
            shares
            cash
            position_value
            portfolio_value
            portfolio_return
    """

    if "close" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'close' column."
        )

    if "position" not in df.columns:
        raise ValueError(
            "DataFrame must contain a 'position' column."
        )

    if initial_capital <= 0:
        raise ValueError(
            "initial_capital must be greater than zero."
        )

    if not 0 < allocation <= 1:
        raise ValueError(
            "allocation must be greater than 0 "
            "and less than or equal to 1."
        )

    result = df.copy()

    cash = float(initial_capital)
    shares = 0
    previous_position = 0

    portfolio_values = []
    cash_values = []
    shares_values = []
    position_values = []

    # Use the first available price for allocation
    initial_price = float(
        result["close"].iloc[0]
    )

    for _, row in result.iterrows():

        price = float(row["close"])
        position = int(row["position"])

        # ------------------------------------------
        # Enter LONG position
        # ------------------------------------------

        if (
            position == 1
            and previous_position != 1
        ):

            allocated_capital = (
                initial_capital * allocation
            )

            shares = int(
                allocated_capital / initial_price
            )

            cash = (
                initial_capital
                - shares * initial_price
            )

        # ------------------------------------------
        # Exit LONG position
        # ------------------------------------------

        elif (
            position != 1
            and previous_position == 1
        ):

            cash += (
                shares * price
            )

            shares = 0

        # ------------------------------------------
        # Calculate portfolio value
        # ------------------------------------------

        position_value = (
            shares * price
        )

        portfolio_value = (
            cash + position_value
        )

        portfolio_values.append(
            portfolio_value
        )

        cash_values.append(
            cash
        )

        shares_values.append(
            shares
        )

        position_values.append(
            position_value
        )

        previous_position = position

    result["shares"] = shares_values

    result["cash"] = cash_values

    result["position_value"] = (
        position_values
    )

    result["portfolio_value"] = (
        portfolio_values
    )

    result["portfolio_return"] = (
        result["portfolio_value"]
        / initial_capital
    ) - 1

    return result