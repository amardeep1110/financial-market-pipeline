import pandas as pd


def clean_market_data(df):
    """
    Clean and validate market data.
    """

    df = df.copy()

    # Convert datetime values.
    # Invalid dates become NaT instead of raising an error.
    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce",
    )

    # Convert numeric columns.
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove rows containing invalid values.
    df = df.dropna(
        subset=[
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    )

    # Sort chronologically.
    df = df.sort_values("datetime")

    # Reset index after cleaning.
    df = df.reset_index(drop=True)

    return df