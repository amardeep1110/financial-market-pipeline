from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.database.models import MarketPrice


def save_market_data(df, symbol, engine):
    """
    Insert new market data or update existing records.
    """

    records = df.to_dict(orient="records")

    records = [
        {
            "symbol": symbol,
            "datetime": record["datetime"],
            "open": record["open"],
            "high": record["high"],
            "low": record["low"],
            "close": record["close"],
            "volume": record["volume"],
            "daily_return": record.get("daily_return"),
            "ma_20": record.get("ma_20"),
            "ma_50": record.get("ma_50"),
            "volatility_20": record.get("volatility_20"),
        }
        for record in records
    ]

    with engine.begin() as connection:

        statement = insert(MarketPrice).values(records)

        update_columns = {
            "open": statement.excluded.open,
            "high": statement.excluded.high,
            "low": statement.excluded.low,
            "close": statement.excluded.close,
            "volume": statement.excluded.volume,
            "daily_return": statement.excluded.daily_return,
            "ma_20": statement.excluded.ma_20,
            "ma_50": statement.excluded.ma_50,
            "volatility_20": statement.excluded.volatility_20,
        }

        statement = statement.on_conflict_do_update(
            constraint="uq_market_symbol_datetime",
            set_=update_columns,
        )

        connection.execute(statement)
def get_market_data(engine, symbol):
    """
    Retrieve processed market data for a symbol.

    Returns:
        pandas.DataFrame: Market data ordered by datetime.
    """
    import pandas as pd

    query = (
        select(MarketPrice)
        .where(MarketPrice.symbol == symbol)
        .order_by(MarketPrice.datetime)
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = result.mappings().all()

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)
