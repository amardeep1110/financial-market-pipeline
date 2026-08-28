import pandas as pd

from config.config import (
    SYMBOL,
    INTERVAL,
    OUTPUT_SIZE,
)
from src.analytics.metrics import (
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from src.database.db import engine
from src.database.repository import save_market_data
from src.ingestion.api_client import fetch_market_data
from src.processing.cleaner import clean_market_data
from src.processing.validator import validate_market_data
from src.transformation.transformer import (
    calculate_daily_returns,
    calculate_moving_averages,
    calculate_volatility,
)
from src.utils.logger import get_logger


logger = get_logger("financial_pipeline")


def run_pipeline(symbol=SYMBOL):
    """
    Run the complete financial market data pipeline.
    """

    logger.info("Starting pipeline for %s", symbol)

    try:
        # 1. Extract
        logger.info("Fetching market data...")
        data = fetch_market_data(
    symbol,
    interval=INTERVAL,
    outputsize=OUTPUT_SIZE,
)

        # 2. Convert JSON to DataFrame
        df = pd.DataFrame(data["values"])
        logger.info("Received %d records", len(df))

        # 3. Clean
        logger.info("Cleaning market data...")
        df = clean_market_data(df)
        logger.info("Records after cleaning: %d", len(df))

        # 4. Validate
        logger.info("Validating market data...")
        validate_market_data(df)
        logger.info("Market data validation passed")

        # 5. Transform
        logger.info("Calculating daily returns...")
        df = calculate_daily_returns(df)

        logger.info("Calculating moving averages...")
        df = calculate_moving_averages(df)

        logger.info("Calculating volatility...")
        df = calculate_volatility(df)

        # 6. Analytics
        sharpe_ratio = calculate_sharpe_ratio(df)
        max_drawdown = calculate_max_drawdown(df)

        logger.info(
            "Sharpe Ratio: %.4f",
            sharpe_ratio if sharpe_ratio is not None else 0,
        )

        logger.info(
            "Maximum Drawdown: %.4f",
            max_drawdown if max_drawdown is not None else 0,
        )

        # 7. Load
        logger.info("Saving data to PostgreSQL...")
        save_market_data(df, symbol, engine)

        logger.info("Data saved successfully")
        logger.info("Pipeline completed successfully")

        return df

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()