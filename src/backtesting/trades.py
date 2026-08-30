import pandas as pd


def generate_trade_log(df):
    """
    Generate a trade-by-trade log from strategy signals.

    A trade starts when position changes from 0 to 1
    and ends when position changes from 1 to 0.

    Returns:
        pandas.DataFrame containing:
            entry_date
            exit_date
            entry_price
            exit_price
            return
            profit_loss
            result
    """

    required_columns = [
        "datetime",
        "close",
        "position",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"DataFrame must contain '{column}' column."
            )

    data = df.copy()

    data["datetime"] = pd.to_datetime(
        data["datetime"]
    )

    trades = []

    in_trade = False
    entry_date = None
    entry_price = None

    for _, row in data.iterrows():

        position = row["position"]

        # ------------------------------------------
        # Enter trade
        # ------------------------------------------

        if position == 1 and not in_trade:

            in_trade = True

            entry_date = row["datetime"]
            entry_price = row["close"]

        # ------------------------------------------
        # Exit trade
        # ------------------------------------------

        elif position == 0 and in_trade:

            exit_date = row["datetime"]
            exit_price = row["close"]

            trade_return = (
                exit_price / entry_price
            ) - 1

            profit_loss = (
                exit_price - entry_price
            )

            result = (
                "WIN"
                if trade_return > 0
                else "LOSS"
            )

            trades.append(
                {
                    "entry_date": entry_date,
                    "exit_date": exit_date,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "return": trade_return,
                    "profit_loss": profit_loss,
                    "result": result,
                }
            )

            in_trade = False

    # ------------------------------------------
    # Handle open trade
    # ------------------------------------------

    if in_trade:

        last_row = data.iloc[-1]

        exit_date = last_row["datetime"]
        exit_price = last_row["close"]

        trade_return = (
            exit_price / entry_price
        ) - 1

        profit_loss = (
            exit_price - entry_price
        )

        result = (
            "WIN"
            if trade_return > 0
            else "LOSS"
        )

        trades.append(
            {
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "return": trade_return,
                "profit_loss": profit_loss,
                "result": result,
            }
        )

    return pd.DataFrame(trades)
