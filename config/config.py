import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# --------------------------------------------------
# API Configuration
# --------------------------------------------------

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

if not API_KEY:
    raise ValueError(
        "TWELVE_DATA_API_KEY is not configured."
    )


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://localhost:5432/market_data",
)


# --------------------------------------------------
# Market Data Configuration
# --------------------------------------------------

SYMBOL = os.getenv(
    "SYMBOL",
    "AAPL",
)

INTERVAL = os.getenv(
    "INTERVAL",
    "1day",
)

OUTPUT_SIZE = int(
    os.getenv(
        "OUTPUT_SIZE",
        "100",
    )
)