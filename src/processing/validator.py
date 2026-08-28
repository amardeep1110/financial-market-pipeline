def validate_market_data(df):
    """
    Validate cleaned market data.

    Returns:
        bool: True if the data is valid.
    """

    required_columns = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    # Check required columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Check for missing values
    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Market data contains missing values."
        )

    # Prices must be positive
    price_columns = [
        "open",
        "high",
        "low",
        "close",
    ]

    if (df[price_columns] <= 0).any().any():
        raise ValueError(
            "Market prices must be greater than zero."
        )

    # Volume cannot be negative
    if (df["volume"] < 0).any():
        raise ValueError(
            "Volume cannot be negative."
        )

    # High must be >= Open and Close
    if (df["high"] < df["open"]).any():
        raise ValueError(
            "High price cannot be lower than open price."
        )

    if (df["high"] < df["close"]).any():
        raise ValueError(
            "High price cannot be lower than close price."
        )

    # Low must be <= Open and Close
    if (df["low"] > df["open"]).any():
        raise ValueError(
            "Low price cannot be higher than open price."
        )

    if (df["low"] > df["close"]).any():
        raise ValueError(
            "Low price cannot be higher than close price."
        )

    return True
