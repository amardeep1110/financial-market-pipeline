import pandas as pd
from config.config import SYMBOL
from src.analytics.metrics import (
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from src.database.db import engine
from src.database.repository import save_market_data
from src.ingestion.api_client import fetch_market_data
from src.processing.cleaner import clean_market_data
from src.transformation.transformer import (
    calculate_daily_returns,
    calculate_moving_averages,
    calculate_volatility,
)

# Step 1: Extract data
data = fetch_market_data(SYMBOL, outputsize=100)

# Step 2: Convert JSON to DataFrame
df = pd.DataFrame(data["values"])

# Step 3: Clean data
df = clean_market_data(df)

# Step 4: Calculate daily returns
df = calculate_daily_returns(df)

# Step 5: Calculate moving averages
df = calculate_moving_averages(df)

# Step 6: Calculate volatility
df = calculate_volatility(df)

sharpe_ratio = calculate_sharpe_ratio(df)

max_drawdown = calculate_max_drawdown(df)

print("\nAnalytics:")
print("Sharpe Ratio:", sharpe_ratio)
print("Maximum Drawdown:", max_drawdown)

# Step 7: Save processed data to PostgreSQL
save_market_data(df, SYMBOL, engine)

print("\nData saved to PostgreSQL successfully!")

print(df)
